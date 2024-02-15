import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from trainer import train_model
from config import Config

class ConversationModel:
    def __init__(self, config):
        self.config = config
        self.model, self.tokenizer = self.initialize_model()

    def is_model_directory_valid(self):
        # Check if the directory exists and contains the required files
        return os.path.exists(self.config.model_directory) and \
               all(os.path.isfile(os.path.join(self.config.model_directory, file)) 
                   for file in self.config.required_files)

    def initialize_model(self):
        if self.is_model_directory_valid():
            print("Loading the trained model...")
            tokenizer = GPT2Tokenizer.from_pretrained(self.config.model_directory)
            model = GPT2LMHeadModel.from_pretrained(self.config.model_directory).to(self.config.device)
        else:
            print("Training a new model...")
            tokenizer = GPT2Tokenizer.from_pretrained(self.config.model_name)
            model = GPT2LMHeadModel.from_pretrained(self.config.model_name).to(self.config.device)
            self.train_model(model, tokenizer)
        return model, tokenizer

    def train_model(self, model, tokenizer):
        train_model(model, tokenizer, self.config)

    def continue_conversation(self, conversation_history):
        # Encode the conversation history and generate the continuation
        input_ids = self.tokenizer.encode(conversation_history, return_tensors='pt').to(self.config.device)
        max_length = len(input_ids[0]) + 500
        generated_text_ids = self.model.generate(
            input_ids,
            max_length=max_length,
            do_sample=True,
            top_k=70,
            no_repeat_ngram_size=0,
            pad_token_id=self.tokenizer.eos_token_id
        )
        return self.tokenizer.decode(generated_text_ids[0], skip_special_tokens=True)

if __name__ == "__main__":
    config = Config()
    conversation_model = ConversationModel(config)
    conversation_history = "Replace this text with some conversation history."
    generated_text = conversation_model.continue_conversation(conversation_history)
    print(generated_text)
