from rest_framework.pagination import LimitOffsetPagination
from django.conf import settings


"""
Default Pagination class for the API.
"""
class DefaultLimitOffsetPagination(LimitOffsetPagination):
    default_limit = getattr(settings, 'REST_FRAMEWORK', {}).get('PAGE_SIZE')
    min_limit = 1
    max_limit = 100
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    ordering_query_param = 'ordering'
    min_page_size = 1
    max_page_size = 100
    page_size_query_param = 'page_size'    
