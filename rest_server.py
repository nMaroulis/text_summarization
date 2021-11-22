from fastapi import FastAPI, Request
import uvicorn
import sqlite3
import signal, sys
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker,relationship
from text_preprocessing_funcs import generate_summary


HOST_IP = '127.0.0.1'
HOST_PORT = 1234

"""
Initiate Database and create a connector with SQLAlchemy as an ORM
"""
engine = db.create_engine('sqlite:///documents.db', echo = True)
connection = engine.connect()
metadata = db.MetaData()
Base = declarative_base()
DBSession = sessionmaker(bind=engine)
session = DBSession()
session.autocommit == True # commits to DB when flush is used



app = FastAPI()

# The Class representation of the Document Table
class Document(Base):
	__tablename__ = 'Document'
   
	id = Column(Integer, primary_key=True, nullable=False, autoincrement = True)
	body = Column(String)
	summary = Column(String)


def insert_document(b):
	new_doc = Document(body=b)
	session.add(new_doc)
	# session.commit() 	
	session.flush() # use flush so we can get the Id of the inserted document
	doc_id  = new_doc.id
	session.commit() # commit to DB
	return doc_id # will


@app.get("/")
async def root():

	print("REST :: Get /")
	# users = session.query(Document).all()
	# for user in users:
	#    print(user.id, user.body)

	return {"text": "Hello World"}


@app.post("/text")
async def store_text(request: Request):

	print("REST :: Post /text")

	json_param = await request.json()  # parse request json payload
	text_body = json_param['text']  # get json body, should include try/catch excpetion

	doc_id = insert_document(text_body) # get inserted doc id

	return {"document_id": doc_id}


@app.get("/text/summary/{document_id}")
async def get_summary(document_id: int, q: str=None):

	print("REST :: Get /text/summary/",document_id)
	doc = session.query(Document).get(document_id)

	if doc is not None: # check if the query returned any result
		summary = generate_summary(doc.body, 0.2)  # request the summary of the given text, using 20% of its most important sentences
		summary = summary[1]
	else:
		summary = None

	return {"document_id": document_id, "summary": summary}


def signal_handler(sig, frame):
	# conn.close()
	print('DB :: Database Connection terminated')
	sys.exit(0)


def db_init():
	if not engine.dialect.has_table(connection, "Document"):  # If table don't exist, Create.
		metadata = MetaData(engine)
		# Create a table with the appropriate Columns
		Table("Document", metadata,
			Column('Id', Integer, primary_key=True, nullable=False, autoincrement = True),
			Column('Body', String),
			Column('Summary', String))
		metadata.create_all()	# Implement the creation
		print("DB :: Database created!")
	else:
		print("DB :: Database already initiated!")



def load_model():
	print("NLP :: NLP Model loaded to memory")


if __name__=="__main__":

	signal.signal(signal.SIGINT, signal_handler) # Handle Ctrl+C exit
	db_init()  # initiate database
	load_model() # Load ML model to memory
	uvicorn.run("rest_server:app",host=HOST_IP, port=HOST_PORT, reload=True, debug=True, workers=3) # run server

