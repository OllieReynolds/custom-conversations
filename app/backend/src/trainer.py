from transformers import (
    TextDataset,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments
)
import random
import os

def train_model(model, tokenizer, config):
    # Ensure the output directory exists
    os.makedirs(config.model_directory, exist_ok=True)

    # Load dataset and prepare for training
    print(f"Loading training data from {config.file_path}")
    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=config.file_path,
        block_size=128
    )
    
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    
    training_args = TrainingArguments(
        output_dir=config.model_directory,
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=8,  # Adjust based on GPU memory
        gradient_accumulation_steps=2,  # Use if increasing batch size is not feasible
        fp16=True,  # If GPU supports FP16, use it
        learning_rate=5e-5,  # Adjust as necessary
        warmup_steps=500,  # Adjust based on dataset size and model
        save_steps=10_000,
        save_total_limit=2,
        seed=random.randint(1, 10000),
        load_best_model_at_end=True,  # Load the best model at the end of training
        evaluation_strategy="steps",  # Or "no" to disable evaluation during training
        eval_steps=5000,  # Adjust based on preference
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
    )
    
    # Start the training process
    print("Training the model...")
    trainer.train()
    
    # Save the trained model and tokenizer
    model.save_pretrained(config.model_directory)
    tokenizer.save_pretrained(config.model_directory)
    print(f"Model saved to {config.model_directory}")

# This can be used to run training from the command line or as a module import.
if __name__ == "__main__":
    from config import Config
    from model import ConversationModel

    # Create config and model instances
    config = Config()
    conversation_model = ConversationModel(config)
    
    # Extract model and tokenizer from the conversation model
    model, tokenizer = conversation_model.model, conversation_model.tokenizer
    
    # Start the training
    train_model(model, tokenizer, config)
