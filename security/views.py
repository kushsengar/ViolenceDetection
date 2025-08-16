# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import ThreatAlert
# from .serializers import ThreatAlertSerializer
# from tensorflow.keras.models import load_model
# import cv2
# import time
# import threading
# from asgiref.sync import async_to_sync
# import json
# from channels.layers import get_channel_layer
# from django.http import StreamingHttpResponse
# from django.views.decorators import gzip
# from collections import deque
# import numpy as np
# import os
# import matplotlib.pyplot as plt
# from pymongo import MongoClient
# import uuid
# from urllib.parse import quote_plus
# # ✅ Fix: Use raw string (r"") for Windows paths
# MODEL_PATH = r"C:\Users\Anuj Kumar\Desktop\PROJECT VOILENCE\backend\security\model.keras"
# database_username = "anujjsengar"
# database_password = "Anuj@082004"

# encoded_username_database = quote_plus(database_username)
# encoded_password_database = quote_plus(database_password)
# mongodb_uri = f"mongodb+srv://{encoded_username_database}:{encoded_password_database}@anujjsengar.2ordy.mongodb.net/demo?retryWrites=true&w=majority"
# # mongodb_uri="mongodb+srv://anujjsengar:anujjsengar@anujjsengar.2ordy.mongodb.net/?retryWrites=true&w=majority&appName=anujjsengar"
# client = MongoClient(mongodb_uri)
# db=client['test']
# collection=db['threatalerts']
# # ✅ Fix: Load model safely
# if os.path.exists(MODEL_PATH):
#     model = load_model(MODEL_PATH)
#     print("Model loaded successfully!")
# else:
#     raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

# # ✅ Save Threat Alert to the database
# @api_view(['POST'])
# def save_threat_alert(request):
#     serializer = ThreatAlertSerializer(data=request.data)  
#     if serializer.is_valid():  
#         serializer.save()  
#         return Response({"message": "Threat alert saved successfully!", "data": serializer.data}, status=201)
#     return Response(serializer.errors, status=400)

# # ✅ Get all Threat Alerts
# @api_view(['GET'])
# def get_threat_alerts(request):
#     alerts = ThreatAlert.objects.all()  
#     serializer = ThreatAlertSerializer(alerts, many=True)  
#     return Response(serializer.data)  

# # ✅ Function to capture live video feed
# def video_feed():
#     cap = cv2.VideoCapture(0)  
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         _, jpeg = cv2.imencode('.jpg', frame)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

# @gzip.gzip_page
# def live_video_stream(request):
#     return StreamingHttpResponse(video_feed(), content_type="multipart/x-mixed-replace; boundary=frame")

# # ✅ Queue for storing predictions
# Q = deque(maxlen=1024)

# # ✅ Process video for violence detection
# def process_video():
#     cap = cv2.VideoCapture(0)
#     total_voilence=0
#     total=0
#     while True:
#         print("Next Interation")
#         time.sleep(5)  # Process every 5 seconds
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         try:
#             # Resize and preprocess frame
#             frame_resized = cv2.resize(frame, (128, 128)).astype("float32")
#             frame_resized = frame_resized.reshape(128, 128, 3) / 255.0
#             #cv2.imshow(frame_resized);
#             # Make prediction
#             preds = model.predict(np.expand_dims(frame_resized, axis=0))[0]
#             Q.append(preds)
#             results = np.array(Q).mean(axis=0)
#             label = (preds > 0.56)[0]  # Violence detected or not
#             total=total+1
#             # ✅ Fix: Save to database if violence is detected
#             if label:
#                 total_voilence+=1
                
                
                
#             # ✅ Fix: Send prediction via WebSocket
#             channel_layer = get_channel_layer()
#             async_to_sync(channel_layer.group_send)(
#                 "live_predictions",
#                 {"type": "send_prediction", "message": json.dumps({"violence_detected": bool(label)})}
#             )

#             print(f"Prediction: Violence Detected = {bool(label)}")

#         except Exception as e:
#             print(f"Error processing frame: {e}")
#             break
#         if(total==5):
#             print((total_voilence*1.0)/total)
#             if((total_voilence*1.0)/total>0.65):
#                 # print((total_voilence*1.0)/total)
#                 print("Overall Last 5 frame Voilence",True)
#                 alert=ThreatAlert.objects.create(
#                     image_url="https//:example.com",
#                     latitude=23.5,
#                     longitude=34.34,
#                     address=95.33
#                 )
#                 alert.save()

#                 mongo_alert = {
#                     "threat_id": str(uuid.uuid4()),  # Generates a unique ID
#                     "image_url": "https://example.com",
#                     "latitude": 23.5,
#                     "longitude": 34.34,
#                     "address": "J BLOCK,GLA UNIVERSITY,MATHURA"  # Replace with actual address
#                 }

#                 collection.insert_one(mongo_alert)
#             else:
#                 print("Overall Last 8 frame Voilence",False)
#             total=0
#             total_voilence=0
# # ✅ Fix: Ensure threading does not block Django
# thread = threading.Thread(target=process_video, daemon=True)
# thread.start()
