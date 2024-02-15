import json

# Specify the encoding as utf-8 when opening the file
with open('./backend/input/matthew_unprocessed.json', encoding='utf-8') as file:
    data = json.load(file)

output_file = './backend/input/matthew_processed.json'

with open(output_file, 'w', encoding='utf-8') as output:
    for message in data["messages"]:
        if "from" not in message:
            continue  # Skip this iteration if 'from' is not in the message

        from_text = message["from"]
        text_entities = message.get("text_entities", [])
        if text_entities:
            text = text_entities[0].get("text", "")
            output.write(f"{from_text}: {text}\n")
        else:
            output.write(f"{from_text}\n")
