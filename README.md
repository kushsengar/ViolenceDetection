Violence Detection & Threat Alert System 🚨
📌 Overview
This project is a real-time violence detection system that uses deep learning, computer vision, and Django REST Framework. The system captures video frames from a camera, processes them through a pre-trained TensorFlow model, and detects if violence is present. If violence is detected, it:

Saves a Threat Alert to the database (Postgres/SQLite via Django ORM + MongoDB for logging).

Sends real-time WebSocket updates to connected clients.

Streams the live video feed via Django.

⚡ Features
🎥 Live Video Streaming with OpenCV and Django.

🤖 Violence Detection Model (TensorFlow/Keras).

📡 WebSocket Integration (via Django Channels) for real-time alerts.

🗄 Dual Database Support:

Django ORM (ThreatAlert model).

MongoDB for logging alerts with unique IDs.

🔄 Background Threading for continuous frame analysis.

📊 Frame Queue to smooth predictions across multiple frames.

🛠 Tech Stack
Backend: Django + Django REST Framework

WebSockets: Django Channels

Database: Django ORM (SQLite/Postgres) + MongoDB

Computer Vision: OpenCV

Deep Learning: TensorFlow / Keras

Threading: Python threading for non-blocking video processing

📂 Project Structure
backend/
│── security/
│   ├── models.py           # ThreatAlert model (Django ORM)
│   ├── serializers.py      # Serializer for ThreatAlert API
│   ├── views.py            # API views + video processing + WebSockets
│   └── model.keras         # Pretrained violence detection model
│
└── manage.py
🚀 How It Works
Video Capture

OpenCV continuously captures frames from the webcam.

Frames are resized & normalized before being fed into the model.

Prediction

TensorFlow model classifies frames (violence or not).

Results are smoothed over the last few frames using a queue.

Alert System

If violence is detected consistently:

Save a ThreatAlert entry in Django ORM.

Insert an alert document into MongoDB (with UUID).

Broadcast prediction to WebSocket clients.

Streaming

A live video stream is provided via Django StreamingHttpResponse.

📡 API Endpoints
POST /save_threat_alert/ → Save a threat alert.

GET /get_threat_alerts/ → Retrieve all saved alerts.

/live_video_stream/ → Live camera stream (MJPEG).

⚙️ Setup & Installation
# Clone repo
git clone https://github.com/your-username/violence-detection.git
cd violence-detection

# Create virtual environment
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

# Install dependencies
pip install -r requirements.txt

# Run Django server
python manage.py runserver
⚠️ Make sure you update your MongoDB credentials in views.py.

📊 Sample Threat Alert Document (MongoDB)
{
  "threat_id": "7d3a12f2-8b8a-4b2d-9a67-bb5a6d22c6a1",
  "image_url": "https://example.com",
  "latitude": 23.5,
  "longitude": 34.34,
  "address": "J BLOCK, GLA University, Mathura"
}
📌 Future Improvements
Add face recognition for identifying people involved.

Integrate mobile notifications (FCM / Twilio SMS).

Deploy model inference on GPU/Edge Devices for faster detection.

Store and analyze alerts in Elasticsearch for threat analytics.
