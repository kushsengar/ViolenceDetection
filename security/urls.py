# from django.urls import path
# # from .views import test_view
# # from .views import save_threat_alert
# # from .views import detect_voilence
# # from .views import get_threat_alerts
# urlpatterns = [
#      #path('test/', test_view, name='test'),  # Example endpoint
#     #path('save-threat/', save_threat_alert, name='save-threat'),
#     path('get_threat_alerts/',get_threat_alerts,name='get-threat-alerts'),
# ]
from django.urls import path
# from .views import save_threat_alert, get_threat_alerts,live_video_stream
from .views2 import process_frame_from_react
urlpatterns = [
    # path('save-threat/', save_threat_alert, name='save-threat'),
    # path('get-threats/', get_threat_alerts, name='get-threats'),
    # path('live-feed/', live_video_stream, name='live_feed'),
    path('process-frame/',process_frame_from_react,name="process_frame")
]
