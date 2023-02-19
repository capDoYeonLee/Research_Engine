from elasticsearch import Elasticsearch
import requests, json, os


directory_path = 'path'
res = requests.get('http://localhost:9200') # 8000
es = Elasticsearch([{'host':'localhost','port':'9200'}])

import requests

headers = {
    'Content-Type': 'application/json'
}

response = requests.post('http://localhost:9200/my-index/_search', headers=headers, json={'query': {'match_all': {}}})

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

                    "id": {
                        "type": "long"
                    },

                    "name": {
                        "type": "text",
                        "analyzer": "my_analyzer"
                    },

                    "about": {
                        "type": "text",
                        "analyzer": "my_analyzer"
                    }

                }
            }
        }
    }
)


dic_path = "C:/Users/ghtyu/OneDrive/Desktop/server_project/search_app/"
with open(dic_path + "dictionary.json", encoding='utf-8') as json_file:
    json_data = json.loads(json_file.read())


body = ""
# count = 1
for i in json_data:
    body = body + json.dumps({"index": {"_index": "dictionary", "_type": "dictionary_datas"}}) + '\n'
    body = body + json.dumps(i, ensure_ascii=False) + '\n'
    # if count == 1:
    # count += 1


#
f = open(dic_path+'input.json', 'w')
f.write(body)
f.close()


es = Elasticsearch()

with open('dictionary.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

for doc in json_data:
    es.index(index='dictionary', body=doc)

from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
indices = es.cat.indices(v=True)
print(indices + "check")


print("바디 테스트 입니다."+body)
es.bulk(body)




