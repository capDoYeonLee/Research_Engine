from datetime import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from elasticsearch import Elasticsearch
import json
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, connections

# Elasticsearch 연결
# connections.create_connection(hosts=['localhost'])
#
# # Elasticsearch 인덱스 및 매핑 정의
# class MyDocument(Document):
#     title = Text(analyzer='snowball', fields={'raw': Keyword()})
#     body = Text(analyzer='snowball')
#     timestamp = Date()
#     author_id = Integer()
#
#     class Index:
#         name = 'dictionary'
#         settings = {
#             'number_of_shards': 1,
#             'number_of_replicas': 0
#         }
# MyDocument.init()
#
# # Elasticsearch에 데이터 추가
# doc = MyDocument(title='My Title', body='Some text', timestamp=datetime.now(), author_id=1)
# doc.save()

class SearchView(APIView):

    def get(self, request):
        es = Elasticsearch([{'host':'localhost','port':'9200'}],timeout=30)

        # 검색어
        search_word = request.query_params.get('search')
        if not search_word:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'search word param is missing'})

        try:
            path = "C:/Users/ghtyu/OneDrive/Desktop/server_project/search_app/"
            with open(path+'dictionary.json', 'r', encoding='utf-8') as f:
                json_data = json.load(f)

            for doc in json_data:
                es.index(index='dictionary', body=doc)

            docs = es.search(index='dictionary',  # index를 잘 못 설정해주는거 같은데
                             body={
                                 "query": {
                                     "multi_match": {
                                         "query": search_word,
                                         "fields": ["name", "about"]
                                     }
                                 },
                                 "_source": ["name", "about"]
                             })
            print(docs)
            data_list = docs['hits']['hits']

            return Response(data_list)

        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': f'Search failed: {e}'})
