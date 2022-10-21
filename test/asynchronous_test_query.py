import sys
import requests
import json
from elasticsearch import Elasticsearch
import time

SERVICE_ADD = 'http://localhost:8085/main'

# query = input("please input a ner query:\t")
# query = '任宪韶的毕业院校是?'
query = '姚明的职业是?'

input_data = {}
input_data['query'] = query

json_str = json.dumps(input_data).encode('utf-8').decode('unicode_escape')
print(json_str)

result = requests.post(SERVICE_ADD, json=input_data)
print(result)

res_json = json.loads(result.text)
print(res_json)
