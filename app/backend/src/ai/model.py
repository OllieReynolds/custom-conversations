import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import List
from app.backend.src.ai.trainer import LanguageModelTrainer
from app.backend.src.utils.config import Config
from app.backend.src.utils.logger import get_logger as create_logger

class ChatModel:
    def __init__(self, config: Config, bypass_model_check: bool = False):
        self.config = config
        self.logger = create_logger(__name__)
        self.bypass_model_check = bypass_model_check
        self.model = None
        self.tokenizer = None

    def check_model_directory(self) -> bool:
        model_config_path = os.path.join(self.config.model_directory, 'config.json')
        return os.path.isfile(model_config_path)

    def setup_model_and_tokenizer(self, for_training=False) -> None:
        if self.check_model_directory() and not for_training:
            self.logger.info("Model found. Loading...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_directory)
            self.model = AutoModelForCausalLM.from_pretrained(self.config.model_directory).to(self.config.device)
        else:
            self.logger.info("Initializing new model for training...")
            self.initialize_new_model_for_training()

    def initialize_new_model_for_training(self) -> None:
        self.logger.info("Initializing new model and tokenizer for training...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.config.model_name, return_dict=True).to(self.config.device)

    def retrain_model(self, training_data: str):
            self.config.file_path = training_data 
            self.logger.info(f"Starting retraining with data from {training_data}")
            self.initialize_new_model_for_training()
            self.train_new_model(self.model, self.tokenizer)

    def train_new_model(self, model: AutoModelForCausalLM, tokenizer: AutoTokenizer):
        trainer = LanguageModelTrainer(model, tokenizer, self.config)
        trainer.execute_training()

    def generate_reply(self, message: str, omit_previous_conversation: bool = True) -> str:
        if not self.model or not self.tokenizer:
            raise Exception("Model and tokenizer must be initialized.")
        input_tensor = self.prepare_input_tensor(message)
        generated_ids = self.generate_response_ids(input_tensor)
        reply_text = self.extract_reply_text(generated_ids, input_tensor, omit_previous_conversation)
        return reply_text

    def prepare_input_tensor(self, message: str) -> List[int]:
        return self.tokenizer.encode(message, return_tensors='pt').to(self.config.device)

    def generate_response_ids(self, input_tensor: List[int]) -> List[int]:
        base_length = len(input_tensor[0])
        max_length_increment = int(self.config.max_length_increment)
        response_length = base_length + max_length_increment
        return self.model.generate(
            input_tensor,
            max_length=response_length,
            do_sample=self.config.do_sample,
            top_k=self.config.top_k,
            no_repeat_ngram_size=self.config.no_repeat_ngram_size,
            pad_token_id=self.tokenizer.eos_token_id,
            temperature=self.config.temperature,
            top_p=self.config.top_p
        )

    def extract_reply_text(self, generated_ids, input_tensor: List[int], omit_previous: bool) -> str:
        start_index = input_tensor.shape[1] if omit_previous else 0
        return self.tokenizer.decode(generated_ids[0][start_index:], skip_special_tokens=True)


if __name__ == "__main__":
    config = app_config
    chat_model = ChatModel(config)
    user_message = "foobar"
    reply = chat_model.generate_reply(user_message)
    chat_model.logger.info(reply)
