import os
from transformers import AutoModelForCausalLM, AutoTokenizer
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
            tokenizer = AutoTokenizer.from_pretrained(self.config.model_directory)
            model = AutoModelForCausalLM.from_pretrained(self.config.model_directory).to(self.config.device)
        else:
            print("Training a new model...")
            tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
            model = AutoModelForCausalLM.from_pretrained(self.config.model_name).to(self.config.device)
            self.train_model(model, tokenizer)
        return model, tokenizer

    def train_model(self, model, tokenizer):
        train_model(model, tokenizer, self.config)

    def continue_conversation(self, conversation_history, hide_conversation_history=True):
        input_ids = self.tokenizer.encode(conversation_history, return_tensors='pt').to(self.config.device)
        max_length = len(input_ids[0]) + 500
        generated_text_ids = self.model.generate(
            input_ids,
            max_length=max_length,
            do_sample=True,
            top_k=50,
            no_repeat_ngram_size=2,
            pad_token_id=self.tokenizer.eos_token_id,
            temperature=0.8,
            top_p=0.92
        )
        if hide_conversation_history:
            new_text_start = input_ids.shape[1]
            return self.tokenizer.decode(generated_text_ids[0][new_text_start:], skip_special_tokens=True)
        else:
            return self.tokenizer.decode(generated_text_ids[0], skip_special_tokens=True)

if __name__ == "__main__":
    config = Config()
    conversation_model = ConversationModel(config)
    conversation_history = "foobar"
    generated_text = conversation_model.continue_conversation(conversation_history)
    print(generated_text)
