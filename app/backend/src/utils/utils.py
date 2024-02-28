import json
from typing import Any, Dict, List
import torch

def check_cuda_available() -> bool:
    return torch.cuda.is_available()

def process_json() -> None:
    input_file_path: str = './backend/input/matthew_unprocessed.json'
    output_file_path: str = './backend/input/matthew_processed.json'

    with open(input_file_path, 'r', encoding='utf-8') as file:
        data: Dict[str, Any] = json.load(file)

    with open(output_file_path, 'w', encoding='utf-8') as output:
        messages: List[Dict[str, Any]] = data.get("messages", [])
        for message in messages:
            from_text: str = message.get("from", "")
            if not from_text:
                continue

            text_entities: List[Dict[str, Any]] = message.get("text_entities", [])
            text: str = ""
            if text_entities:
                text = text_entities[0].get("text", "")

            output_line: str = f"{from_text}: {text}\n" if text else f"{from_text}\n"
            output.write(output_line)

if __name__ == "__main__":
    process_json()
