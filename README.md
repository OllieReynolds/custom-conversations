
# Custom Conversations

## Development

### Frontend

pyinstaller --onefile --hidden-import=paho.mqtt.client --add-data "app/ui/src;app/ui/src" --add-data "app/common/src;app/common/src" app/ui/src/gui.py

### Backend

pyinstaller --onefile --hidden-import=paho.mqtt.client --add-data "app/backend/src;app/backend/src" --add-data "app/common/src;app/common/src" app/backend/src/app.py

### Update `requirements.txt` file

cd app/backend/src
pipreqs . --force

## Usage

### API Endpoints

- **Generate Conversation**
- `GET /generate_conversation`
- Returns a conversation.

- **Check CUDA Availability**
- `GET /check_cuda_available`
- Returns CUDA availability status.

- **Update Configuration**
- `POST /config`
- Body: Configuration JSON
- Updates and returns success status.

- **Get Configuration**
- `GET /config`
- Returns current configuration.
