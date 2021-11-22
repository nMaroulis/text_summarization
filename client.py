from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import uvicorn
import requests
import json

app = FastAPI()
client_html = Jinja2Templates(directory="static/")
SERVER_URL = 'http://127.0.0.1:1234'


@app.get("/")  # returns the client html file, inits the values of the results to '-'
def form_post(request: Request):
	
	txt_id = "-"
	txt_summ = "-"
	return client_html.TemplateResponse('client.html', context={'request': request, 'txt_id': txt_id, 'txt_summary': txt_summ})


@app.post("/submit_id")
def form_post(request: Request, text_id: str= Form(...)):
   
	req = SERVER_URL + "/text/summary/" + text_id
	res = requests.get(req)  # send http get request in order to retrieve the summary for the specified text_id
	
	try:
		
		if res is not None:
			summary = res.json().get("summary") # get summary from json
		else:
			summary = "-"

	except ValueError:  # catch value error in the response
		summary = "-"
		print("REST :: Post /submit_id : JSON Decoding has failed")


	return client_html.TemplateResponse('client.html', context={'request': request, 'txt_summary': summary})



@app.post("/submit_text")
def form_post(request: Request, text_body: str = Form(...)):

	url = SERVER_URL + "/text"

	# send http post for adding the given text in the request's body in the db
	# response should be the Id of the document in the DB

	data = {'text': text_body}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	res = requests.post(url, data=json.dumps(data), headers=headers)
	try:
		if res is not None:
			txt_id = res.json().get("document_id")
			if txt_id is None: # Server returns None in the summary field if the document does not exist
				txt_id = 'Doument Id is not Valid'
		else:
			txt_id = "Error in the server response"
	except ValueError:
		txt_id = "Error in the server response"
		print("REST :: Post /submit_text : JSON Decoding has failed")


	return client_html.TemplateResponse('client.html', context={'request': request, 'txt_id': txt_id})



if __name__=="__main__":

	uvicorn.run("client:app",host='127.0.0.1', port=1235, reload=True, debug=True, workers=3) # run client server

