from db import DB
from services.home_activities import *

db = DB()
db.init_pool()

HomeActivities.run()