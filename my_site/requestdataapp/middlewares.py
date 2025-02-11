from datetime import datetime, timedelta
from http import HTTPStatus

from django.conf import settings
from django.http import HttpRequest, HttpResponse


def set_useragent_on_request_middleware(get_response):
    # print("initial call")

    def middleware(request: HttpRequest) -> HttpResponse:
        # print("before get response")
        request.user_agent = request.META.get("HTTP_USER_AGENT", settings.TEST_USER_AGENT)
        response = get_response(request)
        # print("after get response")
        return response

    return middleware


class CountRequestsMiddleware:

    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.requests_count: int = 0
        self.responses_count: int = 0
        self.exceptions_count: int = 0

    def __call__(self, request: HttpRequest) -> HttpResponse:
        self.requests_count += 1
        # print("request count", self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        # print("response count", self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception) -> None:
        self.exceptions_count += 1
        # print("exception count", self.exceptions_count)


# class TimeRequestMiddleware:

#     def __init__(self, get_response) -> None:
#         self.get_response = get_response
#         self.time_second_request: int = 2
#         self.user_ip_and_time_req: Dict = {}

#     def __call__(self, request: HttpRequest) -> HttpResponse:
#         user_ip: str = self.get_client_ip(request)

#         if user_ip not in self.user_ip_and_time_req:
#             self.user_ip_and_time_req[user_ip] = datetime.now()
#         else:
#             time_diff = (datetime.now() - self.user_ip_and_time_req[user_ip]).total_seconds()

#             if time_diff < self.time_second_request:
#                 raise BadRequest(
#                     f"User ip - {user_ip}, has made a request in less than {self.time_second_request} seconds"
#                 )
#             else:
#                 print(
#                     f"User ip - {user_ip}, made a request more than {self.time_second_request} seconds"
#                 )

#             self.user_ip_and_time_req[user_ip] = datetime.now()

#         response = self.get_response(request)

#         return response

#     def get_client_ip(self, request: HttpRequest) -> str:
#         """Get the client's IP address from the request."""
#         x_forwarded_for: str = request.META.get("HTTP_X_FORWARDED_FOR")

#         if x_forwarded_for:
#             ip: str = x_forwarded_for.split(",")[0]
#         else:
#             ip: str = request.META.get("REMOTE_ADDR")

#         return ip


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.bucket: dict[str, datetime] = {}
        self.rate_ms: int = settings.THROTTLING_RATE_MS

    @classmethod
    def get_client_ip(cls, request: HttpRequest) -> str:
        """Extract the client's IP address from the request."""
        x_forwarded_for: str = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]

        return request.META.get("REMOTE_ADDR", "")

    def request_is_allowed(self, client_ip: str) -> bool:
        """Check if the request from the client IP is allowed based on the rate limit."""
        now: datetime = datetime.now()
        last_access: datetime = self.bucket.get(client_ip)

        if not last_access:
            return True

        if (now - last_access) > timedelta(milliseconds=self.rate_ms):
            return True

        return False

    def __call__(self, request: HttpRequest) -> HttpResponse:
        client_ip = self.get_client_ip(request)
        if self.request_is_allowed(client_ip):
            response = self.get_response(request)
            self.bucket[client_ip] = datetime.now()
        else:
            response = HttpResponse("Rate limit exceeded", status=HTTPStatus.TOO_MANY_REQUESTS)
        return response
