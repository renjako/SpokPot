from modules.database.sqlite import Base
from sqlalchemy import Column, Integer, String, TEXT

class Event(Base):
	__tablename__ = 'events'
	id = Column(Integer, primary_key=True)
	time = Column(String(19))	#format yyyy-mm-dd_hh:mm:ss total 19
	source = Column(String(21))	#format 255.255.255.255:65535 total 21
	request_url = Column(String(500))
	request_raw = Column(TEXT)
	pattern = Column(String(20))
	filename = Column(String(500))

	def __init__(self, time=None, source=None, request_url=None, request_raw=None, pattern=None, filename=None):
		self.time = time
		self.source = source
		self.request_url = request_url
		self.request_raw = request_raw
		self.pattern = pattern
		self.filename = filename

	def __repr__(self):
		return '<Event %r>' % (self.id)