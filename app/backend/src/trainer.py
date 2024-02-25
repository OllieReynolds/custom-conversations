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
            output_dir=self.model_directory,  # Where to save model
            overwrite_output_dir=True,  # Overwrite output directory
            num_train_epochs=self.config.training.num_train_epochs,  # Training epochs
            per_device_train_batch_size=self.config.training.per_device_train_batch_size,  # Batch size per device
            gradient_accumulation_steps=self.config.training.gradient_accumulation_steps,  # Steps before gradient update
            fp16=self.config.training.fp16,  # Use FP16 precision
            learning_rate=self.config.training.learning_rate,  # Learning rate
            warmup_steps=self.config.training.warmup_steps,  # Warmup steps for LR
            save_steps=self.config.training.save_steps,  # Steps to save model
            save_total_limit=self.config.training.save_total_limit,  # Max saved models
            seed=random.randint(1, 10000),  # Random seed for init
            load_best_model_at_end=True,  # Load best model at end
            evaluation_strategy=self.config.training.evaluation_strategy,  # Eval during training
            eval_steps=self.config.training.eval_steps,  # Steps for evaluation
            logging_dir=self.config.training.logging_dir,  # Directory for logs
            logging_steps=self.config.training.logging_steps,  # Steps for logging
            do_train=self.config.training.do_train,  # Whether to train
            do_eval=self.config.training.do_eval,  # Whether to evaluate
            do_predict=self.config.training.do_predict,  # Whether to predict
            logging_strategy="steps",  # Strategy for logging
            save_strategy="steps",  # Strategy for saving
            metric_for_best_model=self.config.training.metric_for_best_model,  # Metric for best model
            greater_is_better=self.config.training.greater_is_better,  # Direction for best metric
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
