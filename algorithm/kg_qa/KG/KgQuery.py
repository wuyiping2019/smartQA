import sys
import requests
import json

SERVICE_ADD = 'http://localhost:8000/kgqa'

while True:
    query = input("please input a query:\t")

    input_data = {}
    input_data['query'] = query
    # input_data['query'] = '任宪韶的毕业院校是?'
    json_str = json.dumps(input_data).encode('utf-8').decode('unicode_escape')
    print(json_str)

    result = requests.post(SERVICE_ADD, json=input_data)
    print(result)
    res_json = json.loads(result.text)

    # print ("QUERY:\t" + input_data['query'])
    print(res_json)

