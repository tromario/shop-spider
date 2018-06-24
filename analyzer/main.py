# coding=utf-8

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# вывод всех записей
# query = {"query": {"match_all": {}}}
# res = es.search(index="products", body=query, size=1000)
# print res

# query = {
#     "query": {
#         "bool": {
#             "must": [
#                 {
#                     "match_phrase": {
#                         "name": "ноутбук черный"
#                     }
#                 }
#             ]
#         }
#     }
# }

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

# query = {
#     "query" : {
#         "constant_score" : {
#             "filter" : {
#                 "term" : {
#                     "name" : "Ноутбук Lenovo Ideapad Y910-17ISK черный"
#                 }
#             }
#         }
#     }
# }

res = es.search(index="products", body=query, size=1000)
print res

print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(name)s - %(price)s" % hit["_source"])