import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from modules.database.sqlite import init_db, db_session
from modules.models.event import Event

# def validateIPv4(ip):
#     ip_regex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$";
#     match = re.search(ip_regex, ip)
#     if match:
#         return True
#     else:
#         return False


# events = Event.query.all()
# for event in events:
# 	if not validateIPv4(event.source):
# 		db_session.delete(event)
		
# db_session.commit()
# print("selesai")


import csv
with open('spokpot.csv')