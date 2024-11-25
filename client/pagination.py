from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    # Set default page size
    page_size = 10
    # Allow clients to set custom page size with `page_size` query parameter
    page_size_query_param = "page_size"
    # Optional: Set a maximum limit for page size
    max_page_size = 100
