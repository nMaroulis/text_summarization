The project is implemented in Python3 with fastAPI for the Rest services and Spacy for the NLP part.


Initiate Environment and Run Server:

1. The virtual environment can be imported using anaconda, with the following commands
	a. Import conda environment from yml file [text_sum_env.yml]
		> conda env create -f text_sum_env.yml
	b. Activate env
		> conda activate text_sum

2. If Conda is not installed the libraries and tools I used are:
	* Python v3.9.7 (older version of python3 should be compatible)
	* FastAPI v0.70 (REST API)
	* Uvicorn v0.15 (ASGI server implementation)
	* SQLAlchemy v1.4.22 (Object–relational mapping with the DB)
	* SQLite3 v 3.36.0 (Lightweight DB for python)
	* Spacy 3.2.0 (for NLP processes)
	* spacy-model-en_core_web_sm v3.2.0 (pre-built model for the english language)
	* jinja2 v2.11.2 and python-multipart v0.0.5 (For the test client's HTML file handling)

3. Files
	a. ./rest_server.py: contains the code and the REST APIs of the server
	b. ./text_preprocessing_funcs.py: contains the NLP model. The function of the summarization is imported and called in the rest server
	c. ./client.py: contains a code for testing the REST server, by also providing a basic GUI
	d. ./static/client.html: contains the UI of the client
	e. ./documents.db: the sqlite3 database, where the documents are stored.
	f. ./ml_model.ipynb: a jupyter notebook file, where i tested the code for the NLP model
	g. ./text_sum_env.yml: a file that contains a python virtual env, which can be imported with conda, creating a venv called text_sum
	h. ./test_rest_server.py: a sample of a testing file for the rest server. 

4. Run the Server and the Client scripts. (If anaconda is not used, specify the version of python after the python command)
	* Start the REST server
		> python rest_server.py
		* The server starts at localhost (127.0.0.1) and port 1234
		* The server script creates a file called document.db which is the sqlite3 database
	* Start the client
		> python client.py
		* The client runs at localhost (127.0.0.1) and port 1235
		* the HTML file can be accessed at [http://127.0.0.1:1235]

5. Instructions
	* The client GUI contains two forms
		* The first is to copy-paste a text, where after pressing 'Submit' it is sent to the server via an HTTP Post request in the   /text uri, inside a json as a payload. Then the GUI will display the document_id, which can be used to retrieve the summary
		* The second form takes as an input an integer which is the document's id that the user wants to retrieve the summary of.

6. Testing
	a. fastAPI has its own tool [fastapi.testclient] in order to write tests for each REST API (see test_rest_server.py for a sample test). Example is testing invalid characters as inputs, expected responses.
	b. In bigger settings, response time could also be measured (e.g. for differenct text sizes -> measure the response time, mainly focusing on the inference time of the ML model)
	c. A python library that could be used is "pytest", which automatically finds test scripts and executes them
	d. As for the NLP, the code could be broken down to smaller functions, where unit testing could be implemented for each specific operation, based on expected output, as well as, processing time. 