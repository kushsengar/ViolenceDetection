from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ThreatAlert
from .serializers import ThreatAlertSerializer
from tensorflow.keras.models import load_model
import cv2
import time
import threading
from asgiref.sync import async_to_sync
import json
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
from collections import deque
import numpy as np
import os
from pymongo import MongoClient
import uuid
from urllib.parse import quote_plus
from django.core.cache import cache
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
# === Model path ===
MODEL_PATH = r"C:\Users\Anuj Kumar\Desktop\PROJECT VOILENCE\backend\security\model.keras"

# === MongoDB Connection ===
database_username = "anujjsengar"
database_password = "Anuj@082004"
encoded_username_database = quote_plus(database_username)
encoded_password_database = quote_plus(database_password)
mongodb_uri = f"mongodb+srv://{encoded_username_database}:{encoded_password_database}@anujjsengar.2ordy.mongodb.net/demo?retryWrites=true&w=majority"
client = MongoClient(mongodb_uri)
db = client['test']
collection = db['threatalerts']

# === Load Keras model ===
if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
    print("Model loaded successfully!")
else:
    raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

# === Global state ===
Q = deque(maxlen=5)
total_violence = 0
total = 0
index = 0
arr = [0, 0, 0, 0, 0]

# === Efficiency checker ===
def efficiency(arr):
    return sum(arr) / 5 >= 0.6
# === Frame processing endpoint ===
@csrf_exempt
def process_frame_from_react(request):
    global total_violence, total, index, arr

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data.get("image")

            if not image_data:
                return JsonResponse({"error": "No image data found"}, status=400)

            # Decode base64 image
            # encoded_data = image_data.split(',')[1]
            # img_data = base64.b64decode(encoded_data)
            # np_arr = np.frombuffer(img_data, np.uint8)
            # frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # if frame is None:
            #     return JsonResponse({"error": "Invalid image"}, status=400)

            # # Resize and preprocess
            # frame_resized = cv2.resize(frame, (128, 128)).astype("float32")
            # frame_resized = frame_resized.reshape(1, 128, 128, 3) / 255.0

            # # Predict using model
            # preds = model.predict(frame_resized)[0]
            # Q.append(preds)
            # results = np.array(Q).mean(axis=0)
            encoded_data = image_data.split(',')[1]
            img_data = base64.b64decode(encoded_data)
            np_arr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if frame is None:
                return JsonResponse({"error": "Invalid image"}, status=400)

            # Optional: Denoising (removes JPEG artifacts, blurs)
            frame = cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 21)

            # Optional: Contrast Limited Adaptive Histogram Equalization (CLAHE)
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            limg = cv2.merge((cl, a, b))
            frame = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

            # Resize and preprocess
            frame_resized = cv2.resize(frame, (128, 128)).astype("float32")
            frame_preprocessed = preprocess_input(frame_resized)  # for MobileNetV2
            frame_preprocessed = frame_preprocessed.reshape(1, 128, 128, 3)

            # Predict using model
            preds = model.predict(frame_preprocessed)[0]
            Q.append(preds)
            results = np.array(Q).mean(axis=0)
            label = results[0] > 0.56  # Violence detected if True

            total += 1
            arr[index] = 1 if label else 0
            index = (index + 1) % 5

            # Broadcast to WebSocket group
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "live_predictions",
                {
                    "type": "send_prediction",
                    "message": json.dumps({"violence_detected": bool(label)})
                }
            )

            # Check if consistent violence detected
            flag = False
            if efficiency(arr):
                arr[0]=0
                arr[1]=0
                arr[2]=0
                arr[3]=0
                arr[4]=0
                # Save to Django DB
                alert = ThreatAlert.objects.create(
                    image_url="https://example.com",  # Replace with actual image URL if available
                    latitude=23.5,
                    longitude=34.34,
                    address="J BLOCK, GLA UNIVERSITY, MATHURA"
                )
                alert.save()

                # Save to MongoDB
                mongo_alert = {
                    "threat_id": str(uuid.uuid4()),
                    "image_url": "https://example.com",
                    "latitude": 23.5,
                    "longitude": 34.34,
                    "address": "J BLOCK, GLA UNIVERSITY, MATHURA"
                }
                collection.insert_one(mongo_alert)

                # Reset counters
                flag = True
                total = 0
                total_violence = 0

            print("Current Frame: violence_detected:", label)
            return JsonResponse({"violence_detected": bool(flag)})

        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method"}, status=405)
