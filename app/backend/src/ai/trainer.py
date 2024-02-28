from transformers import TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments
from transformers import AutoModelForCausalLM, AutoTokenizer
import random
import os
from app.backend.src.utils.config import Config, app_config

class LanguageModelTrainer:
    def __init__(self, model, tokenizer, config: Config):
        self.model = model
        self.tokenizer = tokenizer
        self.config = config
        self.output_directory = config.model_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def prepare_datasets(self):
        full_dataset = TextDataset(
            tokenizer=self.tokenizer,
            file_path=self.config.file_path,
            block_size=128
        )
        
        train_size = int(0.9 * len(full_dataset))
        eval_size = len(full_dataset) - train_size
        
        # Split the dataset into training and evaluation sets
        train_dataset = full_dataset[:train_size]
        eval_dataset = full_dataset[train_size:train_size + eval_size]
        
        return train_dataset, eval_dataset

    
    def prepare_data_collator(self):
        return DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )

    def setup_training_args(self):
        return TrainingArguments(
            output_dir=self.output_directory,
            overwrite_output_dir=True,
            num_train_epochs=self.config.num_train_epochs,
            per_device_train_batch_size=self.config.per_device_train_batch_size,
            gradient_accumulation_steps=self.config.gradient_accumulation_steps,
            fp16=self.config.fp16,
            learning_rate=self.config.learning_rate,
            warmup_steps=self.config.warmup_steps,
            save_steps=self.config.save_steps,
            save_total_limit=self.config.save_total_limit,
            seed=random.randint(1, 10000),
            load_best_model_at_end=True,
            evaluation_strategy="steps",
            eval_steps=self.config.eval_steps,
            logging_dir=self.config.logging_dir,
            logging_steps=self.config.logging_steps,
            do_train=True,
            do_eval=True,
            do_predict=False,
            logging_strategy="steps",
            save_strategy="steps",
            metric_for_best_model=self.config.metric_for_best_model,
            greater_is_better=self.config.greater_is_better,
        )

    def execute_training(self):
        train_dataset, eval_dataset = self.prepare_datasets()
        data_collator = self.prepare_data_collator()
        training_args = self.setup_training_args()
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
        )
        
        trainer.train()
        self.model.save_pretrained(self.output_directory)
        self.tokenizer.save_pretrained(self.output_directory)

if __name__ == "__main__":
    config = app_config
    tokenizer = AutoTokenizer.from_pretrained(config.model_name)
    model = AutoModelForCausalLM.from_pretrained(config.model_name)
    language_model_trainer = LanguageModelTrainer(model, tokenizer, config)
    language_model_trainer.execute_training()
