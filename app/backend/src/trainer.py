from transformers import (
    PreTrainedModel, PreTrainedTokenizer, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments
)
import random
import os
from logger import get_logger
from config_definitions import Config

class ModelTrainer:
    def __init__(self, model: PreTrainedModel, tokenizer: PreTrainedTokenizer, config: Config):
        self.model = model
        self.tokenizer = tokenizer
        self.config = config
        self.logger = get_logger(__name__)
        self.model_directory = config.model_directory
        os.makedirs(self.model_directory, exist_ok=True)

    def load_training_dataset(self) -> TextDataset:
        return TextDataset(
            tokenizer=self.tokenizer,
            file_path=self.config.file_path,
            block_size=128
        )

    def get_data_collator(self) -> DataCollatorForLanguageModeling:
        return DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )

    def get_training_arguments(self) -> TrainingArguments:
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
            seed=random.randint(1, 10000),
            load_best_model_at_end=True,
            evaluation_strategy=self.config.training.evaluation_strategy,
            eval_steps=self.config.training.eval_steps,
            logging_dir=self.config.training.logging_dir,
            logging_steps=self.config.training.logging_steps,
            do_train=self.config.training.do_train,
            do_eval=self.config.training.do_eval,
            do_predict=self.config.training.do_predict,
            logging_strategy="steps",
            save_strategy="steps",
            metric_for_best_model=self.config.training.metric_for_best_model,
            greater_is_better=self.config.training.greater_is_better,
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
        
        trainer.train()
        self.model.save_pretrained(self.model_directory)
        self.tokenizer.save_pretrained(self.model_directory)

if __name__ == "__main__":
    from config import app_config
    from transformers import AutoModelForCausalLM, AutoTokenizer

    config = app_config()
    tokenizer = AutoTokenizer.from_pretrained(config.model.model_name)
    model = AutoModelForCausalLM.from_pretrained(config.model.model_name)
    model_trainer = ModelTrainer(model, tokenizer, config)
    model_trainer.train()
