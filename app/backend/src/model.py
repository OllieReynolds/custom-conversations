import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from trainer import train_model
from config import load_config
from logger import get_logger

class ConversationModel:
    def __init__(self, config):
        self.config = config
        self.logger = get_logger(__name__)
        self.model, self.tokenizer = self.initialize_model()

    def is_model_directory_valid(self):
        return os.path.exists(self.config.model.model_directory) and \
               all(os.path.isfile(os.path.join(self.config.model.model_directory, file))
                   for file in self.config.required_files)

    def initialize_model(self):
        if self.is_model_directory_valid():
            self.logger.info("Loading the trained model...")
            tokenizer = AutoTokenizer.from_pretrained(self.config.model.model_directory)
            model = AutoModelForCausalLM.from_pretrained(self.config.model.model_directory).to(self.config.device)
        else:
            self.logger.info("Training a new model...")
            tokenizer = AutoTokenizer.from_pretrained(self.config.model.model_name)
            model = AutoModelForCausalLM.from_pretrained(self.config.model.model_name).to(self.config.device)
            self.train_model(model, tokenizer)
        return model, tokenizer

    def train_model(self, model, tokenizer):
        train_model(model, tokenizer, self.config)

    def continue_conversation(self, conversation_history, hide_conversation_history=True):
        input_ids = self.tokenizer.encode(conversation_history, return_tensors='pt').to(self.config.device)
        max_length = len(input_ids[0]) + self.config.generation.max_length_increment
        generated_text_ids = self.model.generate(
            input_ids,
            max_length=max_length,
            do_sample=self.config.generation.do_sample,
            top_k=self.config.generation.top_k,
            no_repeat_ngram_size=self.config.generation.no_repeat_ngram_size,
            pad_token_id=self.tokenizer.eos_token_id,
            temperature=self.config.generation.temperature,
            top_p=self.config.generation.top_p
        )
        new_text_start = input_ids.shape[1] if hide_conversation_history else 0
        return self.tokenizer.decode(generated_text_ids[0][new_text_start:], skip_special_tokens=True)

if __name__ == "__main__":
    config = load_config()
    conversation_model = ConversationModel(config)
    conversation_history = "Hello, how are you today?"
    generated_text = conversation_model.continue_conversation(conversation_history)
    conversation_model.logger.info(generated_text)
