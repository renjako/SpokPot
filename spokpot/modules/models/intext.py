from modules.database.sqlite import Base
from sqlalchemy import Column, Integer, String, TEXT

class Intext(Base):
	__tablename__ = 'intext'
	content = Column(String(200), primary_key=True)
	count = Column(Integer)
	firsttime = Column(String(19))
	lasttime = Column(String(19))

	def __init__(self, content=None):
		self.content = content

	def __repr__(self):
		return '<Event %r>' % (self.content)