from transformers import (
    PreTrainedModel, PreTrainedTokenizer, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments
)
import random
import os
from app.backend.src.utils.logger import get_logger
from app.backend.src.utils.config_definitions import Config

class LanguageModelTrainer:
    def __init__(self, model: PreTrainedModel, tokenizer: PreTrainedTokenizer, config: Config):
        self.model = model
        self.tokenizer = tokenizer
        self.config = config
        self.logger = get_logger(__name__)
        self.output_directory = config.model_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def prepare_dataset(self) -> TextDataset:
        return TextDataset(
            tokenizer=self.tokenizer,
            file_path=self.config.file_path,
            block_size=128
        )

    def prepare_data_collator(self) -> DataCollatorForLanguageModeling:
        return DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )

    def setup_training_args(self) -> TrainingArguments:
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
            evaluation_strategy=self.config.evaluation_strategy,
            eval_steps=self.config.eval_steps,
            logging_dir=self.config.logging_dir,
            logging_steps=self.config.logging_steps,
            do_train=self.config.do_train,
            do_eval=self.config.do_eval,
            do_predict=self.config.do_predict,
            logging_strategy="steps",
            save_strategy="steps",
            metric_for_best_model=self.config.metric_for_best_model,
            greater_is_better=self.config.greater_is_better,
        )

    def execute_training(self):
        dataset = self.prepare_dataset()
        data_collator = self.prepare_data_collator()
        training_args = self.setup_training_args()
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=dataset,
        )
        
        trainer.train()
        self.model.save_pretrained(self.output_directory)
        self.tokenizer.save_pretrained(self.output_directory)

if __name__ == "__main__":
    from app.backend.src.utils.config import app_config
    from transformers import AutoModelForCausalLM, AutoTokenizer

    config = app_config
    tokenizer = AutoTokenizer.from_pretrained(config.model_name)
    model = AutoModelForCausalLM.from_pretrained(config.model_name)
    language_model_trainer = LanguageModelTrainer(model, tokenizer, config)
    language_model_trainer.execute_training()
