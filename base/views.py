
from .documents import CookDocument
from .serializers import CookSerializer
from django.http import HttpResponse
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,

    CompoundSearchFilterBackend,
    SimpleQueryStringSearchFilterBackend,
    BaseSearchFilterBackend,
    SearchFilterBackend,
    FacetedSearchFilterBackend,
    MultiMatchSearchFilterBackend,

    OrderingFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination
from elasticsearch_dsl.query import Q, GeoDistance
# from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
# from django.core.management.base import BaseCommand
from .models import Cook


from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_GEO_DISTANCE,
    )
class CookDocumentView(DocumentViewSet):
    document = CookDocument
    serializer_class = CookSerializer
    lookup_field = 'id'
    fielddata = True
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
    ]
    search_fields = (
        'name',
    )

    search_nested_fields = {
        'menu_items': {
            'path': 'menu_items',
            'fields': ['name'],
        }
    }
    multi_match_search_fields = (
       'name',
    )
    filter_fields = {
       'name': 'name'
    }
    ordering_fields = {
        'id': None,
    }
    ordering = ('id')

    geo_spatial_filter_fields = {
        'location': {
        'lookups': [
        LOOKUP_FILTER_GEO_DISTANCE,
        ],
        },
        }

    # def get_queryset(self):
    #     return super().get_queryset()

    def get_queryset(self):

        def handle():
            # create Elasticsearch client
            es = Elasticsearch()

            # define bulk data
            bulk_data = []
            for obj in Cook.objects.all():
                # define document data
                doc = {
                    '_index': 'cook',
                    '_type': '_doc',
                    '_id': obj.id,
                    'name': obj.name,
                    'menu_items': list(obj.menuitems_set.all().values())
                    # add more fields as needed
                }
                bulk_data.append(doc)

            # perform bulk create operation
            success, _ = bulk(es, bulk_data)

            # print results
            print('Bulk create success: %d' % success)

        handle()

        
        search = self.document.search()

    #     # q = Q('prefix', name={'value': s})
    #     print(q)
    #     search = self.document.search().query(q)
    
    # else:
    #     search = self.document.search()
        return search



class SearchProductInventory(APIView, LimitOffsetPagination):
    productinvetory_serializer = CookSerializer
    search_document = CookDocument
    # pagination_class = PageNumberPagination
    # action = 'list'

    # @property
    # def paginator(self):
    #     if not hasattr(self, '_paginator'):
    #         if self.pagination_class is None:
    #             self._paginator = None
    #         else:
    #             self._paginator = self.pagination_class()
    #     else:
    #         pass
    #     return self._paginator
    
    # def paginate_queryset(self, queryset):
    #     if self.paginator is None:
    #         return None
    #     return self.paginator.paginate_queryset(queryset,
    #                self.request, view=self)
    # def get_paginated_response(self, data):
    #     assert self.paginator is not None
    #     return self.paginator.get_paginated_response(data)

    def get(self, request):
        s = self.request.query_params.get('search', None)
        geo_distance = self.request.query_params.get('rad', None)
        location = self.request.query_params.get('loc', None)
        if geo_distance:
            q = Q('bool',
                    filter=GeoDistance(
                        distance=geo_distance,
                        location=location
                    )
                )
            print(q)
            search = self.search_document.search().query(q)
            print('ir'*100)
            print(search)
        elif s:
            # q = Q(
            #     'multi_match',
            #     query=s,
            #     fields=[
            #         'name',
            #     ], fuzziness='auto') 
            # q = {"bool": {
            #     "should": [{
            #         "prefix": {
            #             "name": {
            #                 "value": s
            #             }}
            #         },
            #         {"nested": {
            #          "path": "menu_items",
            #          "query": {
            #                 "bool": {
            #                     "must": [{
            #                         "prefix": {"menu_items.name": s}}
            #                         ]
            #                         }
            #                 }
            #             }
            #         }
            #     ]
            #     }
            # }
            q = Q(
                'bool',
                should=[
                    Q('prefix', name={'value': s}),
                    Q(
                        'nested',
                        path='menu_items',
                        query=Q(
                            'bool',
                            must=[Q('prefix', **{'menu_items.name': s})]
                        )
                    )
                ]
            )
            # & Q(
            #         'nested',path='menu_items',
            #         query='bool', should=[
            #     Q('prefix',{ "menu_items.name": s})
            #         ]
                
            #     )
            print(q)
            search = self.search_document.search().query(q)
            print('ir'*100)
            print(search)
        else:
            search = self.search_document.search()
        # response = search.execute()
        print('hhh')
        # print(response)

        response = search.execute()

        results = self.paginate_queryset(response, request, view=self)
        serializer = self.productinvetory_serializer(results, many=True)
        return self.get_paginated_response(serializer.data)
    

# class Command(BaseCommand):
help = 'Index data in Elasticsearch'
