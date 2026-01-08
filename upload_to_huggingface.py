#!/usr/bin/env python3
"""
Simple upload script for ForeverFit model to Hugging Face
"""

from huggingface_hub import HfApi, create_repo
import os

def upload_model():
    print("=" * 60)
    print("ForeverFit Model Upload to Hugging Face")
    print("=" * 60)
    print()
    
    # Your details
    username = "Ayanmohd1eight"  # Your HF username
    repo_name = "foreverfit-deepseek-lora"
    repo_id = f"{username}/{repo_name}"
    model_path = "./output/foreverfit_lora"
    
    print(f"Username: {username}")
    print(f"Repository: {repo_id}")
    print(f"Model path: {model_path}")
    print()
    
    # Check if model exists
    if not os.path.exists(model_path):
        print(f"❌ Model not found at: {model_path}")
        print("Make sure you have trained the model first!")
        return
    
    print("📤 Starting upload...")
    print("This may take 5-10 minutes depending on your internet speed.")
    print()
    
    try:
        api = HfApi()
        
        # Try to create repo (will skip if exists)
        print("Creating repository...")
        try:
            create_repo(repo_id=repo_id, repo_type="model", exist_ok=True)
            print(f"✅ Repository ready: https://huggingface.co/{repo_id}")
        except Exception as e:
            print(f"Note: {e}")
            print("Continuing with upload...")
        
        print()
        print("Uploading files...")
        
        # Upload folder
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
        print("✅ Next steps:")
        print(f"1. Add to .env file:")
        print(f"   HF_MODEL_REPO={repo_id}")
        print()
        print("2. Test auto-download:")
        print("   python llm_api.py")
        print()
        print("3. Share your GitHub repo!")
        print("   Others will auto-download the model.")
        print()
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ Upload failed!")
        print("=" * 60)
        print()
        print(f"Error: {e}")
        print()
        print("Common fixes:")
        print("1. Check your token has 'Write' permission")
        print("   Go to: https://huggingface.co/settings/tokens")
        print("   Create new token with 'Write' access")
        print()
        print("2. Login again:")
        print("   huggingface-cli login")
        print()
        print("3. Check internet connection")
        print()

if __name__ == "__main__":
    upload_model()
