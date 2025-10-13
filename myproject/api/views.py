from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import ProfileSerializer
from myapp.models import Profile


@api_view(["GET"])
def get_method(requests):
    profile = Profile.objects.all()
    serializer = ProfileSerializer(profile, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def post_method(requests):
    serializer = ProfileSerializer(data=requests.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(["PUT"])
def put_method(requests, pk):
    profile = Profile.objects.get(pk=pk)
    serializer = ProfileSerializer(profile, data=requests.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(["DELETE"])
def delete_method(requests, pk):
    profile = Profile.objects.filter(pk=pk)
    if profile.exists():
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(
        {"error": f"profile does not exist with id: {pk}"},
        status=status.HTTP_404_NOT_FOUND,
    )
