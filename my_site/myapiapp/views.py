from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import GroupSerializer


@api_view(["GET"])
def hello_world_view(request: Request) -> Response:
    return Response({"message": "Hello, World!"})


class GroupsListApiView(ListCreateAPIView):  # type: ignore
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# class GroupsListApiView(ListModelMixin, GenericAPIView):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer

#     def get(self, request: Request) -> Response:
#         return self.list(request)


# class GroupsListApiView(APIView):
#     def get(self, request: Request) -> Response:
#         groups = (
#             Group.objects
#         )  # в данном случае метод all() не нужен, так как при вызове создает копии объекта
#         # data = [group.name for group in groups]
#         group_serializer = GroupSerializer(groups, many=True)
#         return Response({"groups": group_serializer.data})
