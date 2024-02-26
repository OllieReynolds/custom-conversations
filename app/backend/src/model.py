import os
from transformers import AutoModelForCausalLM, AutoTokenizer # type: ignore
from typing import Tuple
from trainer import ModelTrainer
from config import app_config
from config_definitions import Config
from logger import get_logger

class ConversationModel:
    def __init__(self, config: Config):
        self.config = config
        self.logger = get_logger(__name__)
        self.model, self.tokenizer = self.initialize_model()

    def is_model_directory_valid(self) -> bool:
        return os.path.exists(self.config.model_directory) and \
               all(os.path.isfile(os.path.join(self.config.model_directory, file))
                   for file in self.config.required_files)

    def initialize_model(self) -> Tuple[AutoModelForCausalLM, AutoTokenizer]:
        if self.is_model_directory_valid():
            self.logger.info("Loading the trained model...")
            tokenizer: AutoTokenizer = AutoTokenizer.from_pretrained(self.config.model_directory)
            model: AutoModelForCausalLM = AutoModelForCausalLM.from_pretrained(self.config.model_directory).to(self.config.device)
        else:
            self.logger.info("Training a new model...")
            tokenizer = AutoTokenizer.from_pretrained(self.config.model_name) # type: ignore
            model = AutoModelForCausalLM.from_pretrained(self.config.model_name).to(self.config.device) # type: ignore
            self.train_model(model, tokenizer)
        return model, tokenizer

    def train_model(self, model: AutoModelForCausalLM, tokenizer: AutoTokenizer):
        trainer = ModelTrainer(model, tokenizer, self.config)
        trainer.train()

    def continue_conversation(self, conversation_history: str, hide_conversation_history: bool =True) -> str:
        input_ids = self.tokenizer.encode(conversation_history, return_tensors='pt').to(self.config.device)
        max_length = len(input_ids[0]) + self.config.max_length_increment
        generated_text_ids = self.model.generate(
            input_ids,
            max_length=max_length,
            do_sample=self.config.do_sample,
            top_k=self.config.top_k,
            no_repeat_ngram_size=self.config.no_repeat_ngram_size,
            pad_token_id=self.tokenizer.eos_token_id,
            temperature=self.config.temperature,
            top_p=self.config.top_p
        )
        new_text_start = input_ids.shape[1] if hide_conversation_history else 0
        return self.tokenizer.decode(generated_text_ids[0][new_text_start:], skip_special_tokens=True)

if __name__ == "__main__":
    config = app_config
    conversation_model = ConversationModel(config)
    conversation_history = "Hello, how are you?"
    generated_text = conversation_model.continue_conversation(conversation_history)
    conversation_model.logger.info(generated_text)
