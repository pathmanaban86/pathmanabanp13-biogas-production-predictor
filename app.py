"""
Biogas Production Predictor - Hugging Face Gradio App
Interactive ML model for multi-feedstock anaerobic co-digestion
Based on: Pathmanaban et al. (2025) - R² = 0.9887
"""

import gradio as gr
import pandas as pd
import numpy as np
import joblib
import shap
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# LOAD MODEL AND DATA
# ============================================================================

print("Loading model files...")

try:
    model = joblib.load('lightgbm_model.pkl')
    feature_names = joblib.load('feature_names.pkl')
    feature_stats = joblib.load('feature_stats.pkl')
    performance_metrics = joblib.load('performance_metrics.pkl')
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None
    feature_names = None
    feature_stats = None
    performance_metrics = None

try:
    explainer = joblib.load('shap_explainer.pkl')
    print("✅ SHAP explainer loaded")
except:
    if model is not None:
        print("Creating SHAP explainer...")
        explainer = shap.TreeExplainer(model)
        print("✅ SHAP explainer created")
    else:
        explainer = None

# ============================================================================
# PREDICTION FUNCTION
# ============================================================================

def predict_biogas(
    # Feedstocks
    pig_manure, kitchen_waste, chicken_litter, cassava, bagasse,
    energy_grass, banana_shafts, alcohol_waste, municipal_residue, fish_waste,
    # Operational
    water, diesel, electricity, cn_ratio, digester_temp,
    # Climate
    ambient_temp, humidity, rainfall
):
    """Make biogas prediction and generate explanation"""
    
    if model is None:
        return "❌ Model not loaded. Please check setup.", None, None
    
    try:
        # Create input DataFrame
        input_data = {
            'Pig Manure (kg)': pig_manure,
            'Kitchen Food Waste (kg)': kitchen_waste,
            'Chicken Litter (kg)': chicken_litter,
            'Cassava (kg)': cassava,
            'Bagasse Feed (kg)': bagasse,
            'Energy Grass (kg)': energy_grass,
            'Banana Shafts (kg)': banana_shafts,
            'Alcohol Waste (kg)': alcohol_waste,
            'Municipal Residue (kg)': municipal_residue,
            'Fish Waste (kg)': fish_waste,
            'Water (L)': water,
            'Diesel (L)': diesel,
            'Electricity Use (kWh)': electricity,
            'C/N Ratio': cn_ratio,
            'Digester Temp (C)': digester_temp,
            'Temperature (C)': ambient_temp,
            'Humidity (%)': humidity,
            'Rainfall (mm)': rainfall
        }
        
        input_df = pd.DataFrame([input_data])
        input_df = input_df[feature_names]  # Ensure correct order
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        
        # Calculate derived metrics
        daily_energy = prediction * 6.5  # kWh (assuming 6.5 kWh/m³)
        annual_production = prediction * 365 / 1000  # thousand m³/year
        vs_average = prediction - 79.21  # Difference from dataset mean
        
        # Create result text
        result_text = f"""
## 🌱 PREDICTION RESULTS

### Main Output:
**Predicted Biogas Production: {prediction:.2f} m³/day**

### Derived Metrics:
- **Energy Equivalent:** {daily_energy:.1f} kWh/day
- **Annual Production:** {annual_production:.1f} thousand m³/year
- **vs. Facility Average:** {vs_average:+.2f} m³/day ({vs_average/79.21*100:+.1f}%)

### Model Performance:
- Testing R²: 0.9887
- RMSE: 1.17 m³
- MAE: 0.91 m³
- MAPE: 1.15%

---
*Model trained on 15,298 observations over 14 years*
        """
        
        # Calculate SHAP values for explanation
        if explainer is not None:
            try:
                shap_values = explainer.shap_values(input_df)
                
                # Get SHAP contributions
                if len(shap_values.shape) == 1:
                    shap_dict = {name: float(val) for name, val in zip(feature_names, shap_values)}
                else:
                    shap_dict = {name: float(val) for name, val in zip(feature_names, shap_values[0])}
                
                # Sort by absolute value
                sorted_shap = sorted(shap_dict.items(), key=lambda x: abs(x[1]), reverse=True)[:10]
                
                # Create SHAP waterfall plot
                fig = go.Figure(go.Waterfall(
                    name="SHAP",
                    orientation="h",
                    measure=["relative"] * len(sorted_shap),
                    y=[item[0] for item in sorted_shap],
                    x=[item[1] for item in sorted_shap],
                    connector={"line": {"color": "rgb(63, 63, 63)"}},
                    increasing={"marker": {"color": "#2E7D32"}},
                    decreasing={"marker": {"color": "#C62828"}},
                    text=[f"{item[1]:+.2f}" for item in sorted_shap],
                    textposition="outside"
                ))
                
                fig.update_layout(
                    title="Top 10 Feature Contributions (SHAP Values)",
                    xaxis_title="SHAP Value (Impact on Prediction)",
                    yaxis_title="Feature",
                    height=500,
                    showlegend=False,
                    template="plotly_white"
                )
                
                # Create feature importance bar chart
                fig2 = go.Figure(go.Bar(
                    y=[item[0] for item in sorted_shap],
                    x=[abs(item[1]) for item in sorted_shap],
                    orientation='h',
                    marker_color=['#2E7D32' if item[1] > 0 else '#C62828' for item in sorted_shap],
                    text=[f"{abs(item[1]):.2f}" for item in sorted_shap],
                    textposition='outside'
                ))
                
                fig2.update_layout(
                    title="Feature Importance (Absolute SHAP Values)",
                    xaxis_title="Absolute Impact",
                    yaxis_title="Feature",
                    height=500,
                    showlegend=False,
                    template="plotly_white"
                )
                
                return result_text, fig, fig2
                
            except Exception as e:
                print(f"SHAP calculation error: {e}")
                return result_text, None, None
        
        return result_text, None, None
        
    except Exception as e:
        return f"❌ Prediction error: {str(e)}", None, None

# ============================================================================
# BATCH PREDICTION FUNCTION
# ============================================================================

def batch_predict(file):
    """Process CSV file with multiple scenarios"""
    
    if model is None:
        return "❌ Model not loaded", None
    
    if file is None:
        return "❌ Please upload a CSV file", None
    
    try:
        # Read CSV
        df = pd.read_csv(file.name)
        
        # Check if columns match
        missing_cols = set(feature_names) - set(df.columns)
        if missing_cols:
            return f"❌ Missing columns: {missing_cols}", None
        
        # Make predictions
        predictions = []
        for idx, row in df.iterrows():
            input_df = pd.DataFrame([row[feature_names]])
            pred = model.predict(input_df)[0]
            predictions.append(pred)
        
        # Add predictions to dataframe
        df['Predicted_Biogas_m3'] = predictions
        
        # Create summary statistics
        summary = f"""
## 📊 BATCH PREDICTION RESULTS

**Total Scenarios:** {len(df)}

### Summary Statistics:
- **Mean Production:** {np.mean(predictions):.2f} m³/day
- **Std Deviation:** {np.std(predictions):.2f} m³/day
- **Min Production:** {np.min(predictions):.2f} m³/day
- **Max Production:** {np.max(predictions):.2f} m³/day
- **Range:** {np.max(predictions) - np.min(predictions):.2f} m³/day

### Results saved to output file below.
        """
        
        # Create output CSV
        output_file = "biogas_predictions.csv"
        df.to_csv(output_file, index=False)
        
        return summary, output_file
        
    except Exception as e:
        return f"❌ Error processing file: {str(e)}", None

# ============================================================================
# CREATE GRADIO INTERFACE
# ============================================================================

# Get default values (means from dataset)
if feature_stats is not None:
    defaults = feature_stats['means']
else:
    # Fallback defaults
    defaults = {
        'Pig Manure (kg)': 25.10,
        'Kitchen Food Waste (kg)': 17.95,
        'Chicken Litter (kg)': 12.01,
        'Cassava (kg)': 20.03,
        'Bagasse Feed (kg)': 15.09,
        'Energy Grass (kg)': 10.04,
        'Banana Shafts (kg)': 8.01,
        'Alcohol Waste (kg)': 5.02,
        'Municipal Residue (kg)': 11.99,
        'Fish Waste (kg)': 5.99,
        'Water (L)': 99.96,
        'Diesel (L)': 2.00,
        'Electricity Use (kWh)': 25.07,
        'C/N Ratio': 25.00,
        'Digester Temp (C)': 35.96,
        'Temperature (C)': 29.98,
        'Humidity (%)': 74.99,
        'Rainfall (mm)': 4.97
    }

# Get min/max values
if feature_stats is not None:
    mins = feature_stats['mins']
    maxs = feature_stats['maxs']
else:
    # Fallback ranges
    mins = {k: 0.0 for k in defaults.keys()}
    maxs = {
        'Pig Manure (kg)': 60.71,
        'Kitchen Food Waste (kg)': 47.32,
        'Chicken Litter (kg)': 31.29,
        'Cassava (kg)': 49.15,
        'Bagasse Feed (kg)': 38.56,
        'Energy Grass (kg)': 25.42,
        'Banana Shafts (kg)': 21.42,
        'Alcohol Waste (kg)': 12.21,
        'Municipal Residue (kg)': 34.98,
        'Fish Waste (kg)': 14.42,
        'Water (L)': 217.79,
        'Diesel (L)': 5.76,
        'Electricity Use (kWh)': 63.79,
        'C/N Ratio': 36.19,
        'Digester Temp (C)': 42.00,
        'Temperature (C)': 41.70,
        'Humidity (%)': 111.65,
        'Rainfall (mm)': 45.72
    }

# Create Gradio interface with tabs
with gr.Blocks(title="Biogas Production Predictor", theme=gr.themes.Soft()) as demo:
    
    gr.Markdown("""
    # 🌱 Biogas Production Predictor
    
    **Explainable AI Framework for Multi-Feedstock Anaerobic Co-Digestion**
    
    Based on research by Pathmanaban et al. (2025)  
    Model Performance: R² = 0.9887, RMSE = 1.17 m³, MAPE = 1.15%  
    Dataset: 15,298 observations over 14 years (2010-2024)
    
    ---
    """)
    
    with gr.Tabs():
        
        # ===== TAB 1: SINGLE PREDICTION =====
        with gr.TabItem("🎯 Single Prediction"):
            
            gr.Markdown("### Input Feedstock and Operational Parameters")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### 🌾 Feedstocks (kg/day)")
                    pig_manure = gr.Slider(mins['Pig Manure (kg)'], maxs['Pig Manure (kg)'], 
                                          value=defaults['Pig Manure (kg)'], label="Pig Manure")
                    kitchen_waste = gr.Slider(mins['Kitchen Food Waste (kg)'], maxs['Kitchen Food Waste (kg)'], 
                                             value=defaults['Kitchen Food Waste (kg)'], label="Kitchen Food Waste")
                    chicken_litter = gr.Slider(mins['Chicken Litter (kg)'], maxs['Chicken Litter (kg)'], 
                                              value=defaults['Chicken Litter (kg)'], label="Chicken Litter")
                    cassava = gr.Slider(mins['Cassava (kg)'], maxs['Cassava (kg)'], 
                                       value=defaults['Cassava (kg)'], label="Cassava")
                    bagasse = gr.Slider(mins['Bagasse Feed (kg)'], maxs['Bagasse Feed (kg)'], 
                                       value=defaults['Bagasse Feed (kg)'], label="Bagasse Feed")
                
                with gr.Column():
                    gr.Markdown("#### 🌾 More Feedstocks (kg/day)")
                    energy_grass = gr.Slider(mins['Energy Grass (kg)'], maxs['Energy Grass (kg)'], 
                                            value=defaults['Energy Grass (kg)'], label="Energy Grass")
                    banana_shafts = gr.Slider(mins['Banana Shafts (kg)'], maxs['Banana Shafts (kg)'], 
                                             value=defaults['Banana Shafts (kg)'], label="Banana Shafts")
                    alcohol_waste = gr.Slider(mins['Alcohol Waste (kg)'], maxs['Alcohol Waste (kg)'], 
                                             value=defaults['Alcohol Waste (kg)'], label="Alcohol Waste")
                    municipal_residue = gr.Slider(mins['Municipal Residue (kg)'], maxs['Municipal Residue (kg)'], 
                                                 value=defaults['Municipal Residue (kg)'], label="Municipal Residue")
                    fish_waste = gr.Slider(mins['Fish Waste (kg)'], maxs['Fish Waste (kg)'], 
                                          value=defaults['Fish Waste (kg)'], label="Fish Waste")
                
                with gr.Column():
                    gr.Markdown("#### ⚙️ Operational Parameters")
                    water = gr.Slider(mins['Water (L)'], maxs['Water (L)'], 
                                     value=defaults['Water (L)'], label="Water (L)")
                    diesel = gr.Slider(mins['Diesel (L)'], maxs['Diesel (L)'], 
                                      value=defaults['Diesel (L)'], label="Diesel (L)")
                    electricity = gr.Slider(mins['Electricity Use (kWh)'], maxs['Electricity Use (kWh)'], 
                                           value=defaults['Electricity Use (kWh)'], label="Electricity (kWh)")
                    cn_ratio = gr.Slider(mins['C/N Ratio'], maxs['C/N Ratio'], 
                                        value=defaults['C/N Ratio'], label="C/N Ratio")
                    digester_temp = gr.Slider(mins['Digester Temp (C)'], maxs['Digester Temp (C)'], 
                                             value=defaults['Digester Temp (C)'], label="Digester Temp (°C)")
                    
                    gr.Markdown("#### 🌡️ Climate Variables")
                    ambient_temp = gr.Slider(mins['Temperature (C)'], maxs['Temperature (C)'], 
                                            value=defaults['Temperature (C)'], label="Ambient Temp (°C)")
                    humidity = gr.Slider(mins['Humidity (%)'], maxs['Humidity (%)'], 
                                        value=defaults['Humidity (%)'], label="Humidity (%)")
                    rainfall = gr.Slider(mins['Rainfall (mm)'], maxs['Rainfall (mm)'], 
                                        value=defaults['Rainfall (mm)'], label="Rainfall (mm)")
            
            predict_btn = gr.Button("🚀 Predict Biogas Production", variant="primary", size="lg")
            
            with gr.Row():
                output_text = gr.Markdown()
            
            with gr.Row():
                shap_plot = gr.Plot(label="SHAP Feature Contributions")
                importance_plot = gr.Plot(label="Feature Importance")
            
            predict_btn.click(
                fn=predict_biogas,
                inputs=[
                    pig_manure, kitchen_waste, chicken_litter, cassava, bagasse,
                    energy_grass, banana_shafts, alcohol_waste, municipal_residue, fish_waste,
                    water, diesel, electricity, cn_ratio, digester_temp,
                    ambient_temp, humidity, rainfall
                ],
                outputs=[output_text, shap_plot, importance_plot]
            )
        
        # ===== TAB 2: BATCH PREDICTION =====
        with gr.TabItem("📊 Batch Analysis"):
            
            gr.Markdown("""
            ### Upload CSV file for batch predictions
            
            **Required columns:** All 18 features (same names as in Single Prediction tab)
            
            Download the template below to see the required format.
            """)
            
            # Create template CSV
            template_data = {feature: [defaults[feature]] for feature in feature_names}
            template_df = pd.DataFrame(template_data)
            template_csv = template_df.to_csv(index=False)
            
            gr.Markdown("#### Step 1: Download Template")
            gr.File(value=template_csv.encode(), label="CSV Template", file_count="single")
            
            gr.Markdown("#### Step 2: Upload Your Data")
            file_input = gr.File(label="Upload CSV", file_count="single", type="filepath")
            
            batch_btn = gr.Button("🚀 Run Batch Predictions", variant="primary", size="lg")
            
            batch_output = gr.Markdown()
            batch_file = gr.File(label="Download Results")
            
            batch_btn.click(
                fn=batch_predict,
                inputs=[file_input],
                outputs=[batch_output, batch_file]
            )
        
        # ===== TAB 3: ABOUT =====
        with gr.TabItem("ℹ️ About"):
            
            gr.Markdown("""
            ## 📄 Research Paper
            
            This application demonstrates the machine learning framework developed in:
            
            **"Explainable machine learning for multi-feedstock biogas prediction: SHAP-based 
            interaction network analysis and climate effect assessment using long-term operational data"**
            
            *Authors:* Pathmanaban et al.  
            *Year:* 2025  
            *Journal:* [Under Review / To be published]
            
            ---
            
            ## 🎯 Model Performance
            
            | Metric | Value |
            |--------|-------|
            | R² Score | 0.9887 |
            | RMSE | 1.17 m³ |
            | MAE | 0.91 m³ |
            | MAPE | 1.15% |
            
            ---
            
            ## 📊 Dataset Information
            
            **Source:** Indian Biogas Production Prediction Dataset  
            **Provider:** UCI Machine Learning Repository via Kaggle  
            **License:** CC BY 4.0  
            **URL:** [Kaggle Dataset](https://www.kaggle.com/datasets/ucimachinelearning/indian-biogas-production-dataset)
            
            **Characteristics:**
            - 15,298 daily observations
            - 14-year temporal span (2010-2024)
            - 10 organic feedstock types
            - Small-scale plant in India
            - Mesophilic anaerobic digestion
            
            ---
            
            ## 🔬 Key Findings
            
            1. **High Predictive Accuracy:** LightGBM achieved R² = 0.9887
            2. **14 Significant Synergies:** Identified through SHAP interaction analysis
            3. **Pig Manure Centrality:** Highest network centrality (0.556) among feedstocks
            4. **Climate Resilience:** Only 5.02% variance from climate variables
            5. **Operational Stability:** No significant seasonal differences (p = 0.0846)
            
            ---
            
            ## ⚠️ Disclaimer
            
            This model is trained on data from a **single small-scale facility** in India. 
            Predictions should be interpreted as estimates based on historical patterns from that 
            specific facility. Results may vary for other facilities with different:
            - Reactor designs
            - Climate conditions
            - Feedstock quality
            - Operational procedures
            
            **Always validate predictions against your facility's actual performance.**
            
            ---
            
            ## 📧 Contact
            
            **Questions or feedback?**  
            Contact: [pathmanaban13@gmail.com]
            
            **How to cite:**
            ```
            Pathmanaban et al. (2025). Explainable machine learning for multi-feedstock 
            biogas prediction: SHAP-based interaction network analysis and climate effect 
            assessment. [Journal Name]. DOI: [To be added]
            ```
            
            ---
            
            ## 🙏 Acknowledgments
            
            - Dataset: UCI Machine Learning Repository / Kaggle
            - Framework: Gradio, LightGBM, SHAP
            - Platform: Hugging Face Spaces
            
            ---
            
            **Version 1.0** | **Last Updated: February 2025**
            
            © 2025 [Your Institution] | For Research & Educational Purposes
            """)

# Launch the app
if __name__ == "__main__":
    demo.launch()
