"""
Fine-tuning Script for DeepSeek-V3 Medical Chatbot
Uses PEFT (Parameter Efficient Fine-tuning) and TRL for training.
"""

import os
import json
import torch
import argparse
from typing import Dict, List
from datasets import Dataset
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    TaskType
)
from trl import SFTTrainer
import wandb

class MedicalChatbotTrainer:
    """Trainer class for fine-tuning DeepSeek-V3 for medical chatbot responses."""
    
    def __init__(
        self,
        model_name: str = "deepseek-ai/DeepSeek-V3",
        dataset_path: str = "medical_chatbot_dataset.json",
        output_dir: str = "./medical_chatbot_model",
        lora_r: int = 16,
        lora_alpha: int = 32,
        lora_dropout: float = 0.1,
        learning_rate: float = 2e-4,
        num_epochs: int = 3,
        batch_size: int = 4,
        max_seq_length: int = 2048,
        gradient_accumulation_steps: int = 4
    ):
        self.model_name = model_name
        self.dataset_path = dataset_path
        self.output_dir = output_dir
        self.lora_r = lora_r
        self.lora_alpha = lora_alpha
        self.lora_dropout = lora_dropout
        self.learning_rate = learning_rate
        self.num_epochs = num_epochs
        self.batch_size = batch_size
        self.max_seq_length = max_seq_length
        self.gradient_accumulation_steps = gradient_accumulation_steps
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Initialize components
        self.tokenizer = None
        self.model = None
        self.trainer = None

    def load_tokenizer(self):
        """Load and configure the tokenizer."""
        print("Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            padding_side="right"
        )
        
        # Add special tokens for medical chatbot
        special_tokens = {
            "additional_special_tokens": [
                "⚠", "🚨", "🏥", "📋", "⏰", "📍", "🎤", "✅", "❌", "🤕", "💊"
            ]
        }
        self.tokenizer.add_special_tokens(special_tokens)
        
        # Set pad token if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        print(f"Tokenizer loaded. Vocabulary size: {self.tokenizer.vocab_size}")

    def load_model(self):
        """Load and configure the model with LoRA."""
        print("Loading model...")
        
        # Load base model
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            trust_remote_code=True,
            load_in_8bit=True  # Use 8-bit quantization for memory efficiency
        )
        
        # Prepare model for k-bit training
        self.model = prepare_model_for_kbit_training(self.model)
        
        # Configure LoRA
        lora_config = LoraConfig(
            r=self.lora_r,
            lora_alpha=self.lora_alpha,
            target_modules=[
                "q_proj", "k_proj", "v_proj", "o_proj",
                "gate_proj", "up_proj", "down_proj"
            ],
            lora_dropout=self.lora_dropout,
            bias="none",
            task_type=TaskType.CAUSAL_LM
        )
        
        # Apply LoRA
        self.model = get_peft_model(self.model, lora_config)
        self.model.print_trainable_parameters()
        
        # Resize token embeddings if needed
        if self.tokenizer.vocab_size != self.model.config.vocab_size:
            self.model.resize_token_embeddings(self.tokenizer.vocab_size)

    def load_dataset(self) -> Dataset:
        """Load and preprocess the training dataset."""
        print("Loading dataset...")
        
        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        # Convert to format expected by SFTTrainer
        processed_data = []
        for example in raw_data:
            messages = example["messages"]
            
            # Format conversation as a single text
            conversation_text = ""
            for message in messages:
                if message["role"] == "user":
                    conversation_text += f"User: {message['content']}\n"
                else:
                    conversation_text += f"Assistant: {message['content']}\n"
            
            processed_data.append({
                "text": conversation_text.strip(),
                "category": example["category"]
            })
        
        dataset = Dataset.from_list(processed_data)
        print(f"Dataset loaded with {len(dataset)} examples")
        
        # Print some examples
        print("\nExample training data:")
        for i in range(min(2, len(dataset))):
            print(f"\n--- Example {i+1} ---")
            print(dataset[i]["text"][:200] + "...")
        
        return dataset

    def setup_training(self, dataset: Dataset):
        """Setup the training configuration and trainer."""
        print("Setting up training...")
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            num_train_epochs=self.num_epochs,
            per_device_train_batch_size=self.batch_size,
            gradient_accumulation_steps=self.gradient_accumulation_steps,
            learning_rate=self.learning_rate,
            fp16=True,
            logging_steps=10,
            save_steps=500,
            eval_steps=500,
            evaluation_strategy="steps",
            save_total_limit=3,
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            greater_is_better=False,
            warmup_steps=100,
            weight_decay=0.01,
            logging_dir=f"{self.output_dir}/logs",
            report_to="wandb" if wandb.run else None,
            remove_unused_columns=False,
            dataloader_pin_memory=False,
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        # SFT Trainer
        self.trainer = SFTTrainer(
            model=self.model,
            train_dataset=dataset,
            tokenizer=self.tokenizer,
            args=training_args,
            data_collator=data_collator,
            max_seq_length=self.max_seq_length,
            dataset_text_field="text",
            packing=False
        )

    def train(self):
        """Execute the training process."""
        print("Starting training...")
        
        # Initialize wandb if available
        if wandb.run is None:
            try:
                wandb.init(
                    project="medical-chatbot-finetune",
                    name="deepseek-v3-medical",
                    config={
                        "model_name": self.model_name,
                        "lora_r": self.lora_r,
                        "lora_alpha": self.lora_alpha,
                        "learning_rate": self.learning_rate,
                        "num_epochs": self.num_epochs,
                        "batch_size": self.batch_size
                    }
                )
            except Exception as e:
                print(f"Wandb initialization failed: {e}")
        
        # Train the model
        self.trainer.train()
        
        # Save the model
        print("Saving model...")
        self.trainer.save_model()
        self.tokenizer.save_pretrained(self.output_dir)
        
        # Save training config
        config = {
            "model_name": self.model_name,
            "lora_r": self.lora_r,
            "lora_alpha": self.lora_alpha,
            "lora_dropout": self.lora_dropout,
            "learning_rate": self.learning_rate,
            "num_epochs": self.num_epochs,
            "batch_size": self.batch_size,
            "max_seq_length": self.max_seq_length
        }
        
        with open(f"{self.output_dir}/training_config.json", 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Training completed! Model saved to {self.output_dir}")

    def run(self):
        """Run the complete fine-tuning pipeline."""
        try:
            self.load_tokenizer()
            self.load_model()
            dataset = self.load_dataset()
            self.setup_training(dataset)
            self.train()
        except Exception as e:
            print(f"Training failed: {e}")
            raise

def main():
    """Main function to run the fine-tuning."""
    parser = argparse.ArgumentParser(description="Fine-tune DeepSeek-V3 for medical chatbot")
    parser.add_argument("--model_name", default="deepseek-ai/DeepSeek-V3", 
                       help="Base model name")
    parser.add_argument("--dataset_path", default="medical_chatbot_dataset.json",
                       help="Path to training dataset")
    parser.add_argument("--output_dir", default="./medical_chatbot_model",
                       help="Output directory for fine-tuned model")
    parser.add_argument("--lora_r", type=int, default=16,
                       help="LoRA rank")
    parser.add_argument("--lora_alpha", type=int, default=32,
                       help="LoRA alpha")
    parser.add_argument("--learning_rate", type=float, default=2e-4,
                       help="Learning rate")
    parser.add_argument("--num_epochs", type=int, default=3,
                       help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=4,
                       help="Batch size")
    parser.add_argument("--max_seq_length", type=int, default=2048,
                       help="Maximum sequence length")
    
    args = parser.parse_args()
    
    # Create trainer and run training
    trainer = MedicalChatbotTrainer(
        model_name=args.model_name,
        dataset_path=args.dataset_path,
        output_dir=args.output_dir,
        lora_r=args.lora_r,
        lora_alpha=args.lora_alpha,
        learning_rate=args.learning_rate,
        num_epochs=args.num_epochs,
        batch_size=args.batch_size,
        max_seq_length=args.max_seq_length
    )
    
    trainer.run()

if __name__ == "__main__":
    main() 