from django.shortcuts import render


# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from setting_bulk import es
from elasticsearch import Elasticsearch


class SearchView(APIView):

    def get(self, request):
        es = Elasticsearch([{'host':'localhost','port':'9200'}],timeout=30)


        # 검색어
        search_word = request.query_params.get('search')

        if not search_word:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'search word param is missing'})
        print("docs start ============================="+search_word)

        try:
            docs = es.search(index='dictionary',
                             doc_type='dictionary_datas',
                             body={
                                 "query": {
                                     "multi_match": {
                                         "query": search_word,
                                         "fields": ["name", "about"]

                                     }
                                 },
                                 "_source": ["name", "about"]
                             })
            print(docs+"나지롱")

            data_list = docs['hits']['hits']
            return Response(data_list)

        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': f'Search failed: {e}'})

