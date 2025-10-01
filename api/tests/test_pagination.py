import pytest

from django.conf import settings
from rest_framework.test import APIRequestFactory
from api.pagination import DefaultLimitOffsetPagination


@pytest.fixture
def pagination():
    return DefaultLimitOffsetPagination()

def test_default_limit_matches_settings(pagination):
    expected = getattr(settings, 'REST_FRAMEWORK', {}).get('PAGE_SIZE')
    assert pagination.default_limit == expected

def test_limit_query_param(pagination):
    assert pagination.limit_query_param == 'limit'

def test_offset_query_param(pagination):
    assert pagination.offset_query_param == 'offset'

def test_ordering_query_param(pagination):
    assert pagination.ordering_query_param == 'ordering'

def test_min_and_max_limit(pagination):
    assert pagination.min_limit == 1
    assert pagination.max_limit == 100

def test_min_and_max_page_size(pagination):
    assert pagination.min_page_size == 1
    assert pagination.max_page_size == 100

def test_page_size_query_param(pagination):
    assert pagination.page_size_query_param == 'page_size'
