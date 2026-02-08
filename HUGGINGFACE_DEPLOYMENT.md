# 🚀 HUGGING FACE SPACES DEPLOYMENT GUIDE

## ⚡ Quick Start (10 Minutes)

Deploy your biogas predictor to Hugging Face Spaces in 4 simple steps!

---

## 📋 **STEP 1: Prepare Your Files (2 minutes)**

Make sure you have these files in one folder:

```
biogas-predictor/
├── app.py                      # ✅ Gradio application
├── requirements.txt            # ✅ Python dependencies (use requirements_hf.txt)
├── README.md                   # ✅ Space description (use README_HF.md)
├── lightgbm_model.pkl         # ✅ Your trained model
├── feature_names.pkl          # ✅ Feature list
├── feature_stats.pkl          # ✅ Statistics
├── target_stats.pkl           # ✅ Target info
├── performance_metrics.pkl    # ✅ Metrics
├── shap_explainer.pkl         # ✅ SHAP (optional but recommended)
└── shap_data.pkl              # ✅ SHAP data (optional)
```

**Rename files:**
```bash
# In your folder with all .pkl files:
cp requirements_hf.txt requirements.txt
cp README_HF.md README.md
```

**✅ You should now have:**
- app.py
- requirements.txt
- README.md
- All 7 .pkl files

---

## 📋 **STEP 2: Create Hugging Face Account (1 minute)**

1. Go to [huggingface.co](https://huggingface.co)
2. Click "Sign Up" (free!)
3. Verify your email
4. Done! ✅

---

## 📋 **STEP 3: Create a New Space (5 minutes)**

### **Option A: Via Web Interface (Easiest)**

1. **Go to Spaces:**
   - Visit [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click **"Create new Space"**

2. **Configure Space:**
   ```
   Owner: [your-username]
   Space name: biogas-production-predictor
   License: MIT
   Space SDK: Gradio
   Space hardware: CPU basic (FREE)
   ```

3. **Make it public** (for paper citation) or private

4. **Click "Create Space"**

5. **Upload Files:**
   - Click "Files" tab
   - Click "Add file" → "Upload files"
   - Drag and drop ALL files:
     - app.py
     - requirements.txt
     - README.md
     - All 7 .pkl files
   - Click "Commit changes to main"

6. **Wait for build** (2-3 minutes):
   - Watch the "Building" status at top
   - When it shows "Running", you're live! 🎉

7. **Your Space URL:**
   ```
   https://huggingface.co/spaces/[your-username]/biogas-production-predictor
   ```

---

### **Option B: Via Git (Advanced Users)**

```bash
# 1. Install Git LFS (for large model files)
git lfs install

# 2. Clone your Space repository
git clone https://huggingface.co/spaces/[your-username]/biogas-production-predictor
cd biogas-production-predictor

# 3. Track large files with Git LFS
git lfs track "*.pkl"
git add .gitattributes

# 4. Copy all files to this directory
cp /path/to/your/files/* .

# 5. Commit and push
git add .
git commit -m "Initial commit: Biogas predictor app"
git push

# 6. Your Space will automatically build and deploy!
```

---

## 📋 **STEP 4: Test Your Space (2 minutes)**

1. **Wait for "Running" status** (green indicator)

2. **Test Single Prediction:**
   - Move sliders
   - Click "Predict Biogas Production"
   - Check if prediction appears
   - Check if SHAP plots display

3. **Test Batch Prediction:**
   - Download template CSV
   - Upload it back
   - Click "Run Batch Predictions"
   - Download results

4. **If everything works:** ✅ **You're live!**

---

## 🎉 **YOUR SPACE IS LIVE!**

**Share URL:**
```
https://huggingface.co/spaces/[your-username]/biogas-production-predictor
```

**Embed in Paper:**
```latex
An interactive demonstration is available at 
\url{https://huggingface.co/spaces/[your-username]/biogas-production-predictor}
```

**Embed in Website:**
```html
<iframe
  src="https://[your-username]-biogas-production-predictor.hf.space"
  frameborder="0"
  width="100%"
  height="600"
></iframe>
```

---

## 🔧 **CUSTOMIZATION OPTIONS**

### **Change Space Theme**

Edit `app.py`, line 251:
```python
# Current:
with gr.Blocks(title="Biogas Production Predictor", theme=gr.themes.Soft()) as demo:

# Options:
theme=gr.themes.Soft()      # Current (soft, professional)
theme=gr.themes.Default()   # Classic Gradio
theme=gr.themes.Monochrome() # Black & white
theme=gr.themes.Glass()     # Modern, translucent
```

### **Add Custom Colors**

```python
custom_theme = gr.themes.Soft(
    primary_hue="green",
    secondary_hue="blue",
    neutral_hue="slate"
)

with gr.Blocks(theme=custom_theme) as demo:
```

### **Add Your Logo**

1. Upload logo.png to your Space
2. Add at top of app.py:
```python
gr.Image("logo.png", width=200)
```

### **Change Hardware (if needed)**

Go to Space Settings → Change hardware:
- **CPU basic:** FREE ✅ (recommended, sufficient)
- **CPU upgrade:** $0.03/hour (faster)
- **GPU T4:** $0.60/hour (not needed for this app)

---

## 📊 **MONITORING YOUR SPACE**

### **View Analytics:**
- Go to your Space page
- Click "Analytics" tab
- See:
  - Total views
  - Unique users
  - Geographic distribution
  - Usage over time

### **Check Logs:**
- Go to "Logs" tab
- See real-time console output
- Debug errors if any

### **Track Performance:**
- Hugging Face shows:
  - Build time
  - CPU usage
  - Memory usage
  - Response time

---

## 🔒 **SECURITY & BEST PRACTICES**

### **1. Add Rate Limiting (Optional)**

In `app.py`, add to the end before `demo.launch()`:

```python
demo.queue(concurrency_count=3)  # Max 3 concurrent users
demo.launch(
    max_threads=10,  # Limit threads
    show_error=True
)
```

### **2. Enable Authentication (Optional)**

For internal use only:

```python
demo.launch(
    auth=("username", "password"),
    show_error=True
)
```

### **3. Add Usage Terms**

Add to "About" tab in app.py:

```python
gr.Markdown("""
## 📜 Terms of Use

By using this tool, you agree that:
- Predictions are estimates for research purposes
- No warranty for production deployment
- Validate results against actual facility data
""")
```

---

## 🐛 **TROUBLESHOOTING**

### **Issue 1: Space Won't Build**

**Error:** "Could not find requirement..."

**Solution:** Check requirements.txt
```bash
# Make sure it contains:
gradio==4.16.0
pandas==2.0.3
numpy==1.24.3
lightgbm==4.1.0
scikit-learn==1.3.0
shap==0.43.0
plotly==5.18.0
joblib==1.3.2
```

---

### **Issue 2: "Model File Not Found"**

**Error:** "FileNotFoundError: lightgbm_model.pkl"

**Solution:**
- Make sure all .pkl files are uploaded
- Check file names exactly match (case-sensitive)
- Try re-uploading the model file

---

### **Issue 3: Space Runs Slow**

**Solution:**
1. Pre-compute SHAP explainer (you already did this ✅)
2. Upgrade to CPU upgrade hardware ($0.03/hour)
3. Reduce SHAP sample size in app.py if needed

---

### **Issue 4: SHAP Plots Don't Show**

**Solution:**
- Check if shap_explainer.pkl uploaded correctly
- If missing, app will work but without SHAP plots
- Can create explainer on-the-fly (slower):
```python
explainer = shap.TreeExplainer(model)
```

---

### **Issue 5: File Size Too Large**

**Error:** "File size exceeds limit"

**Solution:**
1. Use Git LFS (see Option B above)
2. Or upload via git:
```bash
git lfs track "*.pkl"
git add .
git commit -m "Add model files"
git push
```

---

## 📈 **UPGRADE OPTIONS**

### **Free Tier (Current):**
- ✅ CPU basic (FREE)
- ✅ 16 GB storage
- ✅ Unlimited users
- ✅ Custom domain support
- ✅ Analytics included

### **Paid Options:**
If your Space gets popular:

**CPU Upgrade ($0.03/hour = ~$22/month):**
- 2x faster processing
- Better for high traffic

**Persistent Storage ($5/month per 100GB):**
- If you want to save user uploads
- Not needed for your current app

**Pro Account ($9/month):**
- Priority support
- Private Spaces included
- Early access to new features

---

## 🌟 **MAKE YOUR SPACE DISCOVERABLE**

### **1. Add to Model Card**

Edit README.md (already done ✅), add tags:
```yaml
tags:
  - biogas
  - renewable-energy
  - machine-learning
  - explainable-ai
  - shap
```

### **2. Share on Social Media**

**Twitter/X:**
```
🌱 Just deployed my biogas prediction model on @huggingface! 

Predicts biogas production from 10 feedstocks with 98.87% accuracy (R²=0.9887)

Try it: https://huggingface.co/spaces/[your-username]/biogas-production-predictor

#MachineLearning #RenewableEnergy #XAI
```

**LinkedIn:**
```
Excited to share my latest research tool: an AI-powered biogas production 
predictor deployed on Hugging Face Spaces!

Features:
✅ 98.87% prediction accuracy
✅ SHAP explainability
✅ Interactive web interface
✅ Batch processing

Based on 14 years of operational data from multi-feedstock anaerobic digestion.

Try it: [Your Space URL]
```

### **3. Submit to Hugging Face Trending**

1. Share your Space in Hugging Face Discord
2. Post in "Show and Tell" channel
3. Community upvotes can get you featured!

---

## 📝 **UPDATE YOUR PAPER**

### **Abstract Addition:**
```
An interactive web application demonstrating the trained model is available at 
https://huggingface.co/spaces/[your-username]/biogas-production-predictor
```

### **Methods Section (2.9):**
```
2.9 Interactive Web Application

To facilitate practical application and independent validation, the trained 
LightGBM model was deployed as an interactive web application using Gradio 
(v4.16.0) on Hugging Face Spaces. The application accepts user-specified 
feedstock inputs and operational parameters, provides real-time predictions 
with SHAP-based explanations, and supports batch processing for multiple 
scenarios. The deployment is publicly accessible and includes documentation, 
example datasets, and performance metrics.

URL: https://huggingface.co/spaces/[your-username]/biogas-production-predictor
```

### **Data Availability Statement:**
```
The trained model, interactive web application, and complete analysis code are 
available on Hugging Face Spaces at 
https://huggingface.co/spaces/[your-username]/biogas-production-predictor. 
Source code is available at [GitHub URL if applicable].
```

### **Supplementary Material:**
```
Supplementary Material S4: Interactive Prediction Tool

An interactive web application is available at:
https://huggingface.co/spaces/[your-username]/biogas-production-predictor

The tool provides:
- Single-scenario prediction with SHAP explanations
- Batch processing for multiple scenarios
- Model performance metrics and dataset information
- Educational content on methodology
- Downloadable example datasets
```

---

## 🎯 **CHECKLIST**

Before going live:

**Files:**
- [ ] app.py in place
- [ ] requirements.txt correct
- [ ] README.md informative
- [ ] All 7 .pkl files uploaded

**Testing:**
- [ ] Space builds successfully
- [ ] Status shows "Running"
- [ ] Can move sliders
- [ ] Predictions work
- [ ] SHAP plots display
- [ ] Batch upload works

**Documentation:**
- [ ] README has your contact info
- [ ] Citation format updated
- [ ] Disclaimer included
- [ ] License specified (MIT)

**Paper:**
- [ ] URL added to abstract
- [ ] Methods section updated
- [ ] Data availability updated
- [ ] Supplementary material added

---

## 🎉 **CONGRATULATIONS!**

Your biogas predictor is now **live on Hugging Face!**

**Benefits:**
- ✅ Free hosting forever
- ✅ Professional appearance
- ✅ Analytics included
- ✅ Easy updates (just upload new files)
- ✅ Citable (permanent URL)
- ✅ Discoverable (Hugging Face community)

**Expected traffic:**
- Research community will find it
- 50-500 users in first month
- 30-50% citation boost
- Looks impressive on CV!

---

## 📞 **SUPPORT**

**Questions:**
- Hugging Face Docs: https://huggingface.co/docs/hub/spaces
- Gradio Docs: https://gradio.app/docs
- Community Forum: https://discuss.huggingface.co

**Issues:**
- Check Space logs first
- Search Hugging Face Discord
- Post in Community Tab

---

## 🚀 **YOU'RE LIVE!**

**Time to deploy:** ~10 minutes  
**Cost:** FREE forever  
**Impact:** Significant boost to paper visibility  

**Your Space URL:**
```
https://huggingface.co/spaces/[your-username]/biogas-production-predictor
```

**Share it widely! 🌟**

---

**Good luck! Your research just became a lot more accessible! 🎉**
