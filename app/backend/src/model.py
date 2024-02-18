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
    conversation_history = "Rally walked over to the doberman, his soft argyle dress socks padding on the smooth concrete floor. He stood beside Getson, the doberman’s eyes fixed on Stuart, who was in the middle of opening up his pants slowly. He spread the flaps of his fly, flashing his underwear clad bulge, then flipped them closed again. He zipped up, but left his button and belt undone so that his pants sagged, showing off the waistband of his underwear. Rally grinned at the teasing antics and knelt before Getson. The doberman stared at the show being put on before him, his heart racing. His blood was on fire, every muscle in his body tensed like a spring. Sweat rolled down his muzzle. He couldn’t tear his eyes away, but he could hear his father inside his brain. “You faggot!” He shouted. A mixture of shame and, much to Getson’s surprise, pride sprouted in the doberman’s stomach. His empty stomach did flip flops as arousal, shame and pride crashed together into a ball of emotion inside him. Suddenly, his inner thoughts shattered as pleasure ran down his cock like a lightning bolt. He snapped his eyes away from Stuart’s show for a bare second, looking down to see that Rally had started licking the head of his cock with long slow strokes. Getson groaned. He groaned and his toes curled against the concrete, his eyes rolling. Pleasure shot down his dick from his sensitive knob and went straight to his balls. For two-weeks his fat nuts had held their payload, and now they churned, burning in his sac. Getson tossed his head back, breathing hard through his nose. His cock was so hard it hurt, veins standing out along his shaft like they were ready to burst. "
    generated_text = conversation_model.continue_conversation(conversation_history)
    print(generated_text)
