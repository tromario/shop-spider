# -*- coding: utf-8 -*-

from django.http import JsonResponse
from elasticsearch import Elasticsearch


def index(request):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    query = {
        "query": {
            "match": {
                "name": {
                    "query": "Ноутбук Lenovo Ideapad Y910-17ISK черный",
                    "fuzziness": "AUTO",
                    "prefix_length": 1
                }
            }
        }
    }
    res = es.search(index="products", body=query, size=1000)
    return JsonResponse(res)