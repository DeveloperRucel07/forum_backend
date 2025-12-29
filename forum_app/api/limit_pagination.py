from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class LikesPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10
    
class LikesLimitOffset(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 20