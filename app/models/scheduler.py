# -----------------------------------
#      Scheduler Model
# -----------------------------------
from apscheduler.schedulers.background import BackgroundScheduler
from app.views.scheduler import refresh_token

token = BackgroundScheduler(daemon=True)
token.add_job(refresh_token, 'interval', minutes=150)
token.start()