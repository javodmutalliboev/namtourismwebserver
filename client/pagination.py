from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from urllib.parse import urlparse


class CustomPagination(PageNumberPagination):
    # Set default page size
    page_size = 10
    # Allow clients to set custom page size with `page_size` query parameter
    page_size_query_param = "page_size"
    # Optional: Set a maximum limit for page size
    max_page_size = 100

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data["next"] = self.remove_domain(response.data.get("next"))
        response.data["previous"] = self.remove_domain(response.data.get("previous"))
        return response

    def remove_domain(self, url):
        if url:
            parsed_url = urlparse(url)
            path = parsed_url.path.lstrip("/")  # Remove leading slash
            return f"{path}?{parsed_url.query}" if parsed_url.query else path
        return url
