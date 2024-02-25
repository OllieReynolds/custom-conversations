from transformers import (
    TextDataset,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments
)
import random
import os
from logger import get_logger

class ModelTrainer:
    def __init__(self, model, tokenizer, config):
        self.model = model
        self.tokenizer = tokenizer
        self.config = config
        self.logger = get_logger(__name__)
        self.model_directory = config.model.model_directory
        self.ensure_model_directory()

    def ensure_model_directory(self):
        os.makedirs(self.model_directory, exist_ok=True)

    def load_training_dataset(self):
        self.logger.info(f"Loading training data from {self.config.file_path}")
        return TextDataset(
            tokenizer=self.tokenizer,
            file_path=self.config.file_path,
            block_size=128  # TODO: CONFIGURABLE
        )

    def get_data_collator(self):
        return DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False  # TODO: CONFIGURABLE
        )

    def get_training_arguments(self):
        return TrainingArguments(
            output_dir=self.model_directory,
            overwrite_output_dir=True,
            num_train_epochs=self.config.training.num_train_epochs,
            per_device_train_batch_size=self.config.training.per_device_train_batch_size,
            gradient_accumulation_steps=self.config.training.gradient_accumulation_steps,
            fp16=self.config.training.fp16,
            learning_rate=self.config.training.learning_rate,
            warmup_steps=self.config.training.warmup_steps,
            save_steps=self.config.training.save_steps,
            save_total_limit=self.config.training.save_total_limit,
            seed=random.randint(1, 10000),  # TODO: CONFIGURABLE
            load_best_model_at_end=True,  # TODO: CONFIGURABLE
            evaluation_strategy=self.config.training.evaluation_strategy,
            eval_steps=self.config.training.eval_steps,
        )

    def train(self):
        train_dataset = self.load_training_dataset()
        data_collator = self.get_data_collator()
        training_args = self.get_training_arguments()
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=train_dataset,
        )
        
        self.logger.info("Training the model...")
        trainer.train()
        
        self.model.save_pretrained(self.model_directory)
        self.tokenizer.save_pretrained(self.model_directory)
        self.logger.info(f"Model saved to {self.model_directory}")

if __name__ == "__main__":
    from config import load_config
    from transformers import AutoModelForCausalLM, AutoTokenizer

    config = load_config()

    tokenizer = AutoTokenizer.from_pretrained(config.model.model_name)
    model = AutoModelForCausalLM.from_pretrained(config.model.model_name)

    model_trainer = ModelTrainer(model, tokenizer, config)

    model_trainer.train()
