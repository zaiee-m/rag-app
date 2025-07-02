import requests

url = 'http://127.0.0.1:5000/upload_document'
files = {'file': open('./docs_files/python.txt', 'rb')}
r = requests.post(url=url, files=files)
print(r.json())