#!/usr/bin/env python3
"""
Upload ForeverFit Fine-Tuned Model to Hugging Face Hub
Run this once to share your model with the world (FREE)
"""

from huggingface_hub import HfApi, login
import os

def upload_model():
    print("=" * 60)
    print("ForeverFit Model Upload to Hugging Face")
    print("=" * 60)
    print()
    
    # Step 1: Login
    print("Step 1: Login to Hugging Face")
    print("Get your token from: https://huggingface.co/settings/tokens")
    print()
    
    try:
        login()
        print("✅ Login successful!")
    except Exception as e:
        print(f"❌ Login failed: {e}")
        print("Run: huggingface-cli login")
        return
    
    print()
    
    # Step 2: Get username
    username = input("Enter your Hugging Face username: ").strip()
    if not username:
        print("❌ Username required!")
        return
    
    # Step 3: Upload
    model_path = "./output/foreverfit_lora"
    repo_id = f"{username}/foreverfit-deepseek-lora"
    
    if not os.path.exists(model_path):
        print(f"❌ Model not found at: {model_path}")
        return
    
    print()
    print(f"📤 Uploading model to: {repo_id}")
    print("This may take a few minutes...")
    print()
    
    try:
        api = HfApi()
        
        # Create repo if doesn't exist
        try:
            api.create_repo(repo_id=repo_id, repo_type="model", exist_ok=True)
            print(f"✅ Repository created: https://huggingface.co/{repo_id}")
        except:
            pass
        
        # Upload files
        api.upload_folder(
            folder_path=model_path,
            repo_id=repo_id,
            repo_type="model",
            commit_message="Upload ForeverFit fine-tuned LoRA adapters"
        )
        
        print()
        print("=" * 60)
        print("🎉 SUCCESS! Model uploaded!")
        print("=" * 60)
        print()
        print(f"Model URL: https://huggingface.co/{repo_id}")
        print()
        print("Next steps:")
        print(f"1. Update local_llm_handler.py:")
        print(f"   Change: self.lora_repo = '{repo_id}'")
        print()
        print("2. Share your GitHub repo!")
        print("   Others will auto-download the model on first run.")
        print()
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        print()
        print("Troubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify you're logged in: huggingface-cli whoami")
        print("3. Check model path exists: ./output/foreverfit_lora")

if __name__ == "__main__":
    upload_model()
