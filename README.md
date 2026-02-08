---
title: Biogas Production Predictor
emoji: 🌱
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 4.16.0
app_file: app.py
pinned: false
license: mit
tags:
  - biogas
  - renewable-energy
  - machine-learning
  - explainable-ai
  - shap
  - anaerobic-digestion
  - lightgbm
---

# 🌱 Biogas Production Predictor

**Explainable AI Framework for Multi-Feedstock Anaerobic Co-Digestion**

Interactive machine learning application for predicting biogas production from multiple organic feedstocks using LightGBM and SHAP explainability.

## 📊 Model Performance

- **R² Score:** 0.9887
- **RMSE:** 1.17 m³
- **MAE:** 0.91 m³
- **MAPE:** 1.15%

Trained on 15,298 daily observations over 14 years (2010-2024) from a small-scale biogas plant in India processing 10 different feedstock types.

## 🎯 Features

### Single Prediction Mode
- Interactive sliders for 18 input features
- Real-time biogas production prediction
- SHAP-based feature contribution analysis
- Visual waterfall charts showing prediction breakdown

### Batch Analysis Mode
- Upload CSV files for multiple scenarios
- Automatic batch processing
- Statistical summaries and visualizations
- Download results to CSV

## 📖 Research Paper

This application demonstrates the machine learning framework developed in:

> **"Explainable machine learning for multi-feedstock biogas prediction: SHAP-based interaction network analysis and climate effect assessment using long-term operational data"**

*Authors:* Pathmanaban et al.  
*Year:* 2025  
*Status:* Under Review

## 🔬 Key Findings

1. **High Predictive Accuracy:** LightGBM achieved R² = 0.9887 on testing set
2. **14 Significant Synergies:** Identified through SHAP interaction analysis
3. **Pig Manure as Keystone Substrate:** Highest network centrality (0.556)
4. **Climate Resilience:** Only 5.02% variance attributed to climate variables
5. **Operational Stability:** No significant seasonal production differences (p = 0.0846)

## 📊 Dataset

**Source:** Indian Biogas Production Prediction Dataset  
**Provider:** UCI Machine Learning Repository via Kaggle  
**License:** CC BY 4.0  
**URL:** [Kaggle Dataset](https://www.kaggle.com/datasets/ucimachinelearning/indian-biogas-production-dataset)

**Characteristics:**
- 15,298 daily observations
- 14-year temporal span (2010-2024)
- 10 organic feedstock types
- Small-scale mesophilic anaerobic digester
- Location: India

## 🚀 Usage

### Single Prediction

1. Navigate to the "Single Prediction" tab
2. Adjust sliders for:
   - **Feedstocks (kg/day):** Pig manure, kitchen waste, cassava, etc.
   - **Operational parameters:** Water, diesel, electricity, C/N ratio, temperatures
   - **Climate variables:** Ambient temperature, humidity, rainfall
3. Click "Predict Biogas Production"
4. View results:
   - Predicted biogas production (m³/day)
   - Energy equivalent (kWh/day)
   - Annual production estimate
   - SHAP feature contributions
   - Visual explanations

### Batch Analysis

1. Download the CSV template provided
2. Fill in multiple scenarios
3. Upload your CSV file
4. Click "Run Batch Predictions"
5. Download results with predictions

## 🔧 Technical Details

**Machine Learning:**
- Algorithm: LightGBM (Light Gradient Boosting Machine)
- Features: 18 inputs (10 feedstocks + 5 operational + 3 climate)
- Training: 12,238 observations (80% temporal split)
- Testing: 3,060 observations (20% holdout)

**Explainability:**
- Method: SHAP (SHapley Additive exPlanations)
- Analysis: Feature importance + interaction effects
- Visualization: Waterfall plots, bar charts

**Deployment:**
- Framework: Gradio 4.16.0
- Platform: Hugging Face Spaces
- GPU: Not required (CPU sufficient)

## ⚠️ Disclaimer

This model is trained on data from a **single small-scale facility** in India with specific operational characteristics. Predictions should be interpreted as estimates based on historical patterns from that facility.

**Recommendations:**
- Use predictions as guidance, not absolute values
- Validate with your facility's historical data
- Consider site-specific factors (reactor design, climate, feedstock quality)
- Consult biogas engineering experts for operational decisions

## 📚 How to Cite

```bibtex
@article{pathmanaban2025biogas,
  title={Explainable machine learning for multi-feedstock biogas prediction: 
         SHAP-based interaction network analysis and climate effect assessment},
  author={Pathmanaban and Co-authors},
  journal={[Journal Name]},
  year={2025},
  note={Under Review}
}
```

## 📧 Contact

**Questions or feedback?**  
Email: pathmanaban13@gmail.com

**GitHub Repository:** [Link to your repo]

## 🙏 Acknowledgments

- **Dataset:** UCI Machine Learning Repository / Kaggle
- **Frameworks:** Gradio, LightGBM, SHAP, Plotly
- **Platform:** Hugging Face Spaces
- **License:** MIT License

---

**Built with ❤️ for the renewable energy and AI research community**

*Last Updated: February 2025 | Version 1.0*
