# 🚀 Complete Hugging Face Deployment Guide
# Follow these steps EXACTLY in order

## STEP 1: Create Hugging Face Account (2 minutes)

1. Go to: https://huggingface.co/join
2. Sign up with email (FREE account)
3. Verify your email
4. ✅ Done!

---

## STEP 2: Get Your Access Token (1 minute)

1. Go to: https://huggingface.co/settings/tokens
2. Click "New token"
3. Name it: "ForeverFit Upload"
4. Type: Select "Write"
5. Click "Generate"
6. **COPY THE TOKEN** (you'll need it in next step)
7. ✅ Keep this token safe!

---

## STEP 3: Login to Hugging Face CLI (1 minute)

Open PowerShell in your project folder and run:

```powershell
cd d:\Fitness-AI-Trainer-....V1\FOREVERFIT
.\venv_py310\Scripts\huggingface-cli login
```

When prompted:
- Paste your token (from Step 2)
- Press Enter
- You should see: "Login successful"

✅ You're now logged in!

---

## STEP 4: Upload Your Model (5-10 minutes)

Run the upload script:

```powershell
.\venv_py310\Scripts\python upload_model_to_hf.py
```

When prompted:
- Enter your Hugging Face username (the one you created in Step 1)
- Wait for upload to complete
- You'll see: "🎉 SUCCESS! Model uploaded!"

✅ Your model is now on Hugging Face!

---

## STEP 5: Update Your Code (1 minute)

After upload completes, you'll see a message like:
```
Model URL: https://huggingface.co/YOUR_USERNAME/foreverfit-deepseek-lora
```

### Update .env file:
Add this line to your `.env` file:
```env
HF_MODEL_REPO=YOUR_USERNAME/foreverfit-deepseek-lora
```
(Replace YOUR_USERNAME with your actual Hugging Face username)

✅ Configuration updated!

---

## STEP 6: Test Auto-Download (Optional)

To verify it works:

```powershell
# 1. Rename your local model folder (backup)
Rename-Item .\output\foreverfit_lora .\output\foreverfit_lora_backup

# 2. Start LLM server (should auto-download)
.\venv_py310\Scripts\python llm_api.py

# You should see:
# "📥 Model not found locally. Downloading from Hugging Face..."
# "✅ Model downloaded successfully!"
```

✅ Auto-download works!

---

## STEP 7: Push to GitHub

Now others can use your model!

```powershell
git add .
git commit -m "Add Hugging Face model integration"
git push
```

✅ Deployed!

---

## 🎯 How Others Will Use It:

### When someone clones your repo:

```bash
# 1. Clone
git clone https://github.com/YOUR_GITHUB/Forever-fit.git
cd Forever-fit/FOREVERFIT

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file with:
HF_MODEL_REPO=YOUR_USERNAME/foreverfit-deepseek-lora

# 4. Run LLM server
python llm_api.py
# Model auto-downloads from Hugging Face! ✅

# 5. Run Streamlit (in another terminal)
streamlit run main.py
```

**That's it!** The model downloads automatically on first run.

---

## 📊 What Gets Uploaded:

Your fine-tuned LoRA adapters (~100-500MB):
- `adapter_config.json`
- `adapter_model.safetensors` (or `.bin`)
- Other config files

**NOT uploaded:**
- Base model (users download from DeepSeek directly)
- Your training data
- Your API keys

---

## 🆓 Costs:

- Hugging Face hosting: **FREE**
- Model downloads: **FREE** (unlimited)
- Bandwidth: **FREE** (unlimited)
- Storage: **FREE** (unlimited)

**Total cost: $0 forever!**

---

## ❓ Troubleshooting:

### "Login failed"
- Make sure you copied the FULL token
- Token must have "Write" permission
- Try: `huggingface-cli whoami` to check login

### "Upload failed"
- Check internet connection
- Verify model exists at: `./output/foreverfit_lora`
- Try again (uploads can resume)

### "Model not found" when others try
- Make sure you set `HF_MODEL_REPO` in `.env`
- Verify model is public on Hugging Face
- Check username is correct

---

## 🎉 Success Checklist:

- [ ] Created Hugging Face account
- [ ] Got access token
- [ ] Logged in via CLI
- [ ] Uploaded model successfully
- [ ] Updated .env with HF_MODEL_REPO
- [ ] Tested auto-download
- [ ] Pushed to GitHub

**Once all checked, you're done!** Others can now use your fine-tuned model! 🚀

---

## 🔗 Important Links:

- Your model: `https://huggingface.co/YOUR_USERNAME/foreverfit-deepseek-lora`
- Hugging Face docs: https://huggingface.co/docs/hub
- Get help: https://huggingface.co/docs/hub/repositories-getting-started

---

**Ready to start? Begin with STEP 1!**
