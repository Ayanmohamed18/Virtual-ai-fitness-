import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    BitsAndBytesConfig,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model

# ------------------------
# CONFIG
# ------------------------
MODEL_ID = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
DATA_PATH = "deepseek_fitness_training.json"
OUTPUT_DIR = "./output/foreverfit_lora"

MAX_LENGTH = 1024
BATCH_SIZE = 1
GRAD_ACCUM = 8
EPOCHS = 3
LR = 2e-4

# ------------------------
# LOAD MODEL (4-bit)
# ------------------------
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_ID,
    use_fast=True
)

# IMPORTANT: DeepSeek/Qwen style models need this
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    quantization_config=bnb_config,
    device_map={'': 0},  # Force all layers to GPU 0
    torch_dtype=torch.float16
)

# ------------------------
# APPLY LoRA (behavior tuning)
# ------------------------
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj"
    ]
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# ------------------------
# LOAD DATASET
# ------------------------
dataset = load_dataset(
    "json",
    data_files=DATA_PATH,
    split="train"
)

# ------------------------
# FORMAT CHAT DATA
# ------------------------
def format_example(example):
    text = ""
    for msg in example["messages"]:
        text += f"<|{msg['role']}|>\n{msg['content']}\n"
    return {"text": text}

dataset = dataset.map(
    format_example,
    remove_columns=dataset.column_names
)

# ------------------------
# TOKENIZE
# ------------------------
def tokenize(example):
    return tokenizer(
        example["text"],
        truncation=True,
        max_length=MAX_LENGTH,
        padding=False
    )

dataset = dataset.map(
    tokenize,
    batched=True,
    remove_columns=["text"]
)

# ------------------------
# DATA COLLATOR
# ------------------------
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

# ------------------------
# TRAINING ARGS (STABLE)
# ------------------------
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=GRAD_ACCUM,
    num_train_epochs=EPOCHS,
    learning_rate=LR,
    fp16=True,
    logging_steps=1,
    save_strategy="steps",
    save_steps=5,
    save_total_limit=3,
    report_to="none",
    optim="paged_adamw_8bit",
    remove_unused_columns=False
)

# ------------------------
# TRAINER
# ------------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=data_collator
)

# ------------------------
# TRAIN
# ------------------------
trainer.train()

# ------------------------
# SAVE LoRA ADAPTER
# ------------------------
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print("\n✅ Fine-tuning complete. LoRA adapter saved to:", OUTPUT_DIR)
