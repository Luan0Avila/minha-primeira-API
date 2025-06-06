from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import User
from .serializers import UserSerializer

import json

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):

    if request.method == 'GET':
        users = User.objects.all()  # pega todos os objetos no banco de dados Users

        serializer = UserSerializer(users, many=True)   # serializa os dados dos objetos em json
        return Response(serializer.data)    # vai retornar esses dados serializados
    
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def get_by_nick(request, nick):

    try:
        user = User.objects.get(pk=nick)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':

        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user_manager(request):

    if request.method == 'GET':    

        try:
            if request.GET['user']:      # checa se o parametro é chamado 'user'

                user_nickname = request.GET['user']     # encontra o parametro get

                try:
                    user = User.objects.get(pk=user_nickname)   # pega o objeto no banco de dados
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                
                serializer = UserSerializer(user)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # CRIANDO DADOS
    if request.method == 'POST':

        new_user = request.data
        
        serializer = UserSerializer(data=new_user)

        if serializer.is_valid():   # verifica se o serializer é valido
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # EDITANDO DADOS
    if request.method == 'PUT':

        nickname = request.data['user_nickname']

        try:
            updated_user = User.objects.get(pk=nickname)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        serializer = UserSerializer(updated_user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # DELETAR DADOS
    if request.method == 'DELETE':

        try:
            user_to_delete = User.objects.get(pk=request.data['user_nickname'])
            user_to_delete.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)