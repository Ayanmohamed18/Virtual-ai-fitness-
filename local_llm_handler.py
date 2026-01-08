import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
import threading

class LocalLLMHandler:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(LocalLLMHandler, cls).__new__(cls)
                cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return
            
        self.base_model_id = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
        self.lora_path = "./output/foreverfit_lora"
        self.model = None
        self.tokenizer = None
        
        # Check if we are in Client Mode (Remote URL set)
        import os
        if os.getenv("REMOTE_LLM_URL"):
            print("🚀 Client Mode Detected: Skipping local model load.")
            self.model = None # Stay None
        else:
            # Load model immediately on instantiation only if NOT in client mode
            self._load_model()
            
        self.initialized = True

    def _load_model(self):
        # Double check to prevent accidental loads
        import os
        if os.getenv("REMOTE_LLM_URL"):
            return

        print("🔄 Loading Local LLM (DeepSeek-R1-Distill-Qwen-7B + LoRA)...")
        
        # Auto-download from Hugging Face if model not present
        if not os.path.exists(self.lora_path):
            print("📥 Model not found locally. Downloading from Hugging Face...")
            try:
                from huggingface_hub import snapshot_download
                
                # TODO: Replace with your Hugging Face username after uploading
                # Example: "yourusername/foreverfit-deepseek-lora"
                hf_repo_id = os.getenv("HF_MODEL_REPO", "YOUR_USERNAME/foreverfit-deepseek-lora")
                
                if "YOUR_USERNAME" in hf_repo_id:
                    print("⚠️  Model not uploaded to Hugging Face yet.")
                    print("   Run: python upload_model_to_hf.py")
                    print("   Or set HF_MODEL_REPO in .env")
                    self.model = None
                    return
                
                print(f"   Downloading from: {hf_repo_id}")
                snapshot_download(
                    repo_id=hf_repo_id,
                    local_dir=self.lora_path,
                    local_dir_use_symlinks=False
                )
                print("✅ Model downloaded successfully!")
                
            except ImportError:
                print("❌ huggingface_hub not installed. Run: pip install huggingface_hub")
                self.model = None
                return
            except Exception as e:
                print(f"❌ Failed to download model: {e}")
                print("   Make sure the model is uploaded to Hugging Face Hub")
                self.model = None
                return
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.base_model_id)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
            )

            base_model = AutoModelForCausalLM.from_pretrained(
                self.base_model_id,
                quantization_config=bnb_config,
                torch_dtype=torch.float16,
                device_map={'': 0}  # Force GPU 0
            )

            self.model = PeftModel.from_pretrained(base_model, self.lora_path)
            self.model.eval()
            print("✅ Local LLM loaded successfully!")
        except Exception as e:
            print(f"❌ Failed to load Local LLM: {e}")
            self.model = None

    def generate_response_stream(self, system_prompt: str, user_prompt: str, max_tokens: int = 1024, temperature: float = 0.8):
        if not self.model:
            yield "Error: Local model is not loaded."
            return

        from transformers import TextIteratorStreamer
        from threading import Thread

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)

        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
        
        # Optimized generation parameters for expert-level responses
        generation_kwargs = dict(
            **inputs,
            streamer=streamer,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=0.92,  # Slightly higher for more creative, diverse responses
            top_k=50,  # Add top-k sampling for better quality control
            repetition_penalty=1.15,  # Stronger penalty to avoid repetitive text
            do_sample=True,
            use_cache=True,
            num_beams=1,  # Greedy decoding for speed
            pad_token_id=self.tokenizer.eos_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
        )

        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        for new_text in streamer:
            yield new_text

    def generate_response(self, system_prompt: str, user_prompt: str, max_tokens: int = 1024, temperature: float = 0.8) -> str:
        # Backward compatibility wrapper
        full_response = ""
        for chunk in self.generate_response_stream(system_prompt, user_prompt, max_tokens, temperature):
            full_response += chunk
        return full_response

# Global instance
local_llm = LocalLLMHandler()
