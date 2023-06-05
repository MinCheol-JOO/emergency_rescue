from apscheduler.schedulers.background  import BackgroundScheduler
# from django.utils import timezone
from realtime.views import Emergency_Room_finder

def task_refresh_data_hour():
    # Do something here
    print("Task running... refresh")
    Emergency_Room_finder().refresh_data()
    
def start_scheduler():
    # Create a scheduler instance
    scheduler = BackgroundScheduler()
    # Add a job to the scheduler
    scheduler.add_job(task_refresh_data_hour, 'interval', hours=1)
    # scheduler.add_job(task_refresh_data_hour, 'interval', seconds=5)
    # Start the scheduler
    scheduler.start()