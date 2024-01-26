class DataLoader:
    @staticmethod
    def load_conversation_data(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
        return lines
