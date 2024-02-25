
# Custom Conversations

## Development

### Frontend

pyinstaller --onefile --hidden-import=paho.mqtt.client --add-data "app/ui/src;app/ui/src" --add-data "app/common/src;app/common/src" app/ui/src/gui.py

### Backend

pyinstaller --onefile --hidden-import=paho.mqtt.client --add-data "app/backend/src;app/backend/src" --add-data "app/common/src;app/common/src" app/backend/src/app.py

### Update `requirements.txt` file

cd app/backend/src
pipreqs . --force