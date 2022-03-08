from rest_framework import status, generics
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

from django.contrib.auth.models import User
# from .serializers import RegisterSerializer



@csrf_exempt
@api_view(['GET', 'POST'])
def images_list(request):
    permission_classes = IsAuthenticatedOrReadOnly
    if request.method == 'GET':
        images = Image.objects.all()
        serializer = ImageSerializer(images, context={'request': request}, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def get_image(request, pk):
    """
    Retrieve, update or delete a movie instance.
    """
    try:
        images = Image.objects.get(pk=pk)
    except Image.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ImageSerializer(images, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ImageSerializer(images, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        images.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST'])
def messages_list(request):
    permission_classes = IsAuthenticatedOrReadOnly
    if request.method == 'GET':
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, context={'request': request}, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def get_message(request, pk):
    """
    Retrieve, update or delete a movie instance.
    """
    try:
        messages = Message.objects.get(pk=pk)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MessageSerializer(messages, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MessageSerializer(messages, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        messages.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
