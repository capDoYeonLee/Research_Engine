from elasticsearch import Elasticsearch
import requests, json, os


es = Elasticsearch()

directory_path = 'path'
res = requests.get('http://localhost:9200')
es = Elasticsearch([{'host':'localhost','port':'9200'}])

es.indices.create(
    index='dictionary',
    body={
        "settings": {
            "index": {
                "analysis": {
                    "analyzer": {
                        "my_analyzer": {
                            "type": "custom",
                            "tokenizer": "nori_tokenizer"
                        }
                    }
                }
            }
        },
        "mappings": {
            "dictionary_datas": {
                "properties": {

                    "name": {
                        "type": "text",
                        "analyzer": "my_analyzer"
                    },
                    "about": {
                        "type": "text",
                        "analyzer": "my_analyzer"
                    },
                    "id": {
                        "type": "long"
                    }
                }
            }
        }
    }
)
import json

dic_path = "C:/Users/ghtyu/OneDrive/Desktop/server_project/search_app/"
with open(dic_path + "dictionary.json", encoding='utf-8') as json_file:
    json_data = json.loads(json_file.read())

body = ""
count = 1
for i in json_data:
    body = body + json.dumps({"index": {"_index": "dictionary", "_type": "dictionary_datas"}}) + '\n'
    body = body + json.dumps(i, ensure_ascii=False) + '\n'
    if count == 1:
        print(body)
    count += 1

# 무슨 json import


f = open(dic_path+'input.json', 'w')
f.write(body)
f.close()
es.bulk(body)


