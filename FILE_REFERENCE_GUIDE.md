# 📁 QUICK FILE REFERENCE GUIDE

## 🎯 **FOR HUGGING FACE DEPLOYMENT (What You Requested)**

Upload these files to your Hugging Face Space:

### **Required Files:**
```
📦 Your Hugging Face Space
│
├── app.py                          ⭐ USE THIS (Gradio app)
├── requirements.txt                ⭐ RENAME from requirements_hf.txt
├── README.md                       ⭐ RENAME from README_HF.md
│
├── lightgbm_model.pkl             ✅ From training script
├── feature_names.pkl              ✅ From training script
├── feature_stats.pkl              ✅ From training script
├── target_stats.pkl               ✅ From training script
├── performance_metrics.pkl        ✅ From training script
├── shap_explainer.pkl             ✅ From training script
└── shap_data.pkl                  ✅ From training script
```

### **File Renaming Commands:**
```bash
# Before uploading to Hugging Face:
cp requirements_hf.txt requirements.txt
cp README_HF.md README.md
```

### **Total Files to Upload: 10**
- 1 Python app (app.py)
- 1 requirements file
- 1 README
- 7 model/data files (.pkl)

---

## 📊 **COMPARISON: Hugging Face vs Streamlit**

| Aspect | **Hugging Face** (Your Choice) | Streamlit Cloud |
|--------|-------------------------------|-----------------|
| **Main App File** | `app.py` (Gradio) | `biogas_predictor_app.py` (Streamlit) |
| **Requirements** | `requirements_hf.txt` | `requirements.txt` (original) |
| **README** | `README_HF.md` | `README.md` (original) |
| **Framework** | Gradio 4.16.0 | Streamlit 1.31.0 |
| **Deployment Time** | 5-10 minutes | 5-10 minutes |
| **Cost** | FREE forever | FREE forever |
| **Interface Style** | Simple, ML-focused | More customizable |
| **File Upload** | Via web or git | Via GitHub only |
| **Community** | ML research community | Broader data science |

---

## ✅ **WHAT YOU NEED FOR HUGGING FACE (STEP BY STEP)**

### **Step 1: Gather Files**

From your current directory where you ran `train_and_save_model.py`:

**✅ You already have:**
```
lightgbm_model.pkl           (1.36 MB)
feature_names.pkl            (~1 KB)
feature_stats.pkl            (~2 KB)
target_stats.pkl             (~1 KB)
performance_metrics.pkl      (~1 KB)
shap_explainer.pkl           (4.16 MB)
shap_data.pkl               (4.71 MB)
```

**📥 Download from outputs:**
```
app.py                       (Gradio application)
requirements_hf.txt          (Python dependencies)
README_HF.md                (Space description)
HUGGINGFACE_DEPLOYMENT.md   (Deployment guide)
```

### **Step 2: Rename Files**

```bash
# Copy these files to a new folder called "biogas-predictor-hf"
mkdir biogas-predictor-hf
cd biogas-predictor-hf

# Copy the .pkl files from your training directory
cp /path/to/your/training/*.pkl .

# Copy and rename the HF files
cp /path/to/downloads/app.py .
cp /path/to/downloads/requirements_hf.txt requirements.txt
cp /path/to/downloads/README_HF.md README.md
```

### **Step 3: Verify You Have Everything**

```bash
ls -lh
```

**Expected output:**
```
app.py
requirements.txt
README.md
lightgbm_model.pkl
feature_names.pkl
feature_stats.pkl
target_stats.pkl
performance_metrics.pkl
shap_explainer.pkl
shap_data.pkl
```

**Total: 10 files ✅**

### **Step 4: Upload to Hugging Face**

Follow the **HUGGINGFACE_DEPLOYMENT.md** guide!

---

## 🔄 **IF YOU WANT TO SWITCH TO STREAMLIT LATER**

Use these files instead:

```
📦 Streamlit Cloud
│
├── biogas_predictor_app.py        (Streamlit app)
├── requirements.txt               (Original requirements)
├── README.md                      (Original README)
│
└── [Same 7 .pkl files]
```

**Deployment:** Push to GitHub → Connect Streamlit Cloud

---

## 💡 **RECOMMENDED WORKFLOW**

### **For Paper Submission (Quick & Easy):**

1. ✅ **Use Hugging Face** (what you asked for)
   - Simple Gradio interface
   - Upload files directly via web
   - Live in 10 minutes
   - ML research community

### **For Professional Portfolio:**

2. Later, create Streamlit version too
   - More polished UI
   - Deploy both
   - Different audiences

**You can have BOTH!** They share the same .pkl files.

---

## 📊 **FILE SIZE SUMMARY**

```
app.py                    21 KB
requirements.txt         121 bytes
README.md               4.9 KB
lightgbm_model.pkl      1.36 MB
feature_names.pkl       ~1 KB
feature_stats.pkl       ~2 KB
target_stats.pkl        ~1 KB
performance_metrics.pkl ~1 KB
shap_explainer.pkl      4.16 MB
shap_data.pkl          4.71 MB
─────────────────────────────────
TOTAL:                ~10.23 MB ✅
```

**✅ Well within Hugging Face limits (50 GB)**

---

## 🎯 **DEPLOYMENT CHECKLIST**

**Before Starting:**
- [ ] I ran `train_and_save_model.py` successfully
- [ ] I have all 7 .pkl files
- [ ] I downloaded app.py, requirements_hf.txt, README_HF.md
- [ ] I have a Hugging Face account

**File Preparation:**
- [ ] Created folder `biogas-predictor-hf`
- [ ] Copied all 7 .pkl files
- [ ] Copied app.py
- [ ] Renamed requirements_hf.txt → requirements.txt
- [ ] Renamed README_HF.md → README.md
- [ ] Verified 10 files total

**Hugging Face:**
- [ ] Logged into huggingface.co
- [ ] Created new Space (Gradio SDK)
- [ ] Uploaded all 10 files
- [ ] Waited for "Running" status
- [ ] Tested predictions work
- [ ] Got my Space URL

**Paper:**
- [ ] Added URL to abstract
- [ ] Updated methods section
- [ ] Updated data availability
- [ ] Tested URL in browser

---

## 🚀 **YOUR SPACE URL WILL BE:**

```
https://huggingface.co/spaces/[YOUR-USERNAME]/biogas-production-predictor
```

**Example:**
```
https://huggingface.co/spaces/pathmanaban13/biogas-production-predictor
```

---

## 📞 **QUICK HELP**

**Q: Which files do I upload to Hugging Face?**
A: All 10 files listed in Step 3 above.

**Q: Do I need to install anything locally?**
A: No! Upload files directly via Hugging Face web interface.

**Q: How much does it cost?**
A: FREE forever with CPU basic (sufficient for this app).

**Q: How do I update the app later?**
A: Just upload new files to your Space (they replace old ones).

**Q: Can I test locally first?**
A: Yes! Run `gradio app.py` but you need to install packages first.

**Q: What if a file is missing?**
A: Re-run `train_and_save_model.py` to regenerate .pkl files.

---

## ✅ **YOU'RE READY!**

**Follow this order:**

1. **Read:** HUGGINGFACE_DEPLOYMENT.md (comprehensive guide)
2. **Prepare:** Gather all 10 files
3. **Deploy:** Upload to Hugging Face Space
4. **Test:** Try predictions
5. **Share:** Add URL to your paper!

**Time needed:** 15 minutes total

**Good luck! 🌟**
