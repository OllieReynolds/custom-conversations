import os
import random
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments

class Config:
    def __init__(self, model_directory="./trained_model", model_name="gpt2", file_path='done.txt'):
        self.model_directory = model_directory
        self.required_files = ['config.json']
        self.model_name = model_name
        self.file_path = file_path
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

class DataLoader:
    @staticmethod
    def load_conversation_data(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
        return lines

class ConversationModel:
    def __init__(self, config):
        self.config = config
        self.model, self.tokenizer = self.initialize_model()

    def is_model_directory_valid(self):
        if not os.path.exists(self.config.model_directory):
            return False
        if not all(os.path.isfile(os.path.join(self.config.model_directory, file)) for file in self.config.required_files):
            return False
        return True

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
        train_dataset = TextDataset(tokenizer=tokenizer, file_path=self.config.file_path, block_size=128)
        data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
        training_args = TrainingArguments(
            output_dir=self.config.model_directory,
            overwrite_output_dir=True,
            num_train_epochs=3,
            save_strategy='no',
            seed=random.randint(1, 10000),
        )
        trainer = Trainer(
            model=model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=train_dataset,
        )
        trainer.train()
        model.save_pretrained(self.config.model_directory)
        tokenizer.save_pretrained(self.config.model_directory)

    def continue_conversation(self, conversation_history):
        input_ids = self.tokenizer.encode(conversation_history, return_tensors='pt').to(self.config.device)
        max_length = len(input_ids[0]) + 500
        generated_text_ids = self.model.generate(
            input_ids,
            max_length=max_length,
            do_sample=True,
            top_k=80,
            no_repeat_ngram_size=0
        )
        return self.tokenizer.decode(generated_text_ids[0], skip_special_tokens=True)

# Example usage
config = Config()
conversation_model = ConversationModel(config)
all_lines = DataLoader.load_conversation_data(config.file_path)
num_lines = 20
random_start = random.randint(0, len(all_lines) - num_lines)
selected_lines = all_lines[random_start:random_start + num_lines]
conversation_history = " ".join(selected_lines)
generated_text = conversation_model.continue_conversation(conversation_history)
print(generated_text)
