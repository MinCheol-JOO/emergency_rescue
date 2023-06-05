from django.apps import AppConfig

class RealtimeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'realtime'
    
    def ready(self):
        #서버 준비후 import
        from realtime import scheduler
        # Start the scheduler when the app is ready
        scheduler.start_scheduler()
