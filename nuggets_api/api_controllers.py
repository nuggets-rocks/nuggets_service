from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Nugget
from .serializers import NuggetSerializer
from django.contrib.auth import authenticate


@api_view(['GET'])
def nuggets_to_review_by_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.auth.user != user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        nuggets = Nugget.get_todays_review_nuggets_by_user(user)
        serializer = NuggetSerializer(nuggets, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def nuggets_op_by_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.auth.user != user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        nuggets = Nugget.get_nuggets_by_user(user)
        serializer = NuggetSerializer(nuggets, many=True)
        return Response(serializer.data)

    #TODO: Deprecate in favor of create_new_user?
    #shiva: was running into the following error when calling POST:
    #"creator": [
    #    "This field is required."
    #]
    elif request.method == 'POST':
        serializer = NuggetSerializer(user, data=request.data)
        if serializer.is_valid():
            Nugget.create_new_nugget(user, serializer.validated_data['content'], serializer.validated_data['source'], serializer.validated_data['url'])
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([]) # Don't require a token for calling create_user
@permission_classes([])
def create_new_user(request, user_name, password):
    try:
        # Attempt to fetch existing user
        User.objects.get(username=user_name)
    except User.DoesNotExist:
        user = User.objects.create_user(user_name, 'email-address', password)
        # Auth token which should be supplied from all requests for the user.
        token = Token.objects.get(user_id=user.id)
        return Response({'user_id': user.id, 'token': token.key})
    # else return a client error code
    return Response(status=status.HTTP_409_CONFLICT)


@api_view(['GET'])
@authentication_classes([]) # Don't require a token for calling authenticateUser
@permission_classes([])
def authenticate_user(request, user_name, password):
    user = authenticate(username=user_name, password=password)
    if user is not None:
        token = Token.objects.get(user_id=user.id)
        return Response({'user_id': user.id, 'token': token.key})
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def create_new_nugget(request, user_id, content, source, url):
    try:
        # Check for existing user
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.auth.user != user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    newnugget = Nugget.create_new_nugget(user, content, source, url)

    serializer = NuggetSerializer(newnugget, many=False)
    return Response(serializer.data)


@api_view(['DELETE', 'PUT', 'GET'])
def nuggets_op_by_user_and_nugget(request, user_id, nugget_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.auth.user != user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        nugget = Nugget.objects.get(id=nugget_id)
    except Nugget.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NuggetSerializer(nugget, many=False)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = NuggetSerializer(user, data=request.data)
        if serializer.is_valid():
            return Response(Nugget.update_nugget(user, nugget, serializer.validated_data['content']))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        return Response(Nugget.delete_nugget(user, nugget))
