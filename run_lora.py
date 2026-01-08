import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

BASE_MODEL = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
LORA_PATH = "./output/foreverfit_lora"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

# Use 4-bit config to match training (QLoRA)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

print("Loading base model (4-bit)...")
model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    quantization_config=bnb_config,
    torch_dtype=torch.float16,
    device_map={'': 0} # Force GPU
)

print(f"Loading LoRA adapter from {LORA_PATH}...")
model = PeftModel.from_pretrained(model, LORA_PATH)
model.eval()

print("\n✅ Model loaded successfully!")

# Simple test generation
prompt = "I want to lose fat but also build muscle. Is that even possible?"
messages = [
    {"role": "system", "content": "You are an expert Personal Trainer."},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)

print(f"\nUser: {prompt}\nAI Generating...")
with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=200)
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))
