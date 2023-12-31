#from django.shortcuts import render
from rest_framework import status
from rest_framework import generics, viewsets, mixins
#from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from .models import Account, Users
from .serializers import AccountSerializer, AccountSerializerRegistr
from django.utils.crypto import get_random_string
from rest_framework.generics import get_object_or_404
from .services import create_account_number  
#from django.http.request import QueryDict
#import uuid
from rest_framework import generics, viewsets, mixins, filters
#from django.db import IntegrityError
#from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError


class AccountList(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = AccountSerializer
    #lookup_url_kwargs = 'username'
    queryset = Account.objects.all()
    
     

class AccountCreate(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Account.objects.all()
    serializer_class = AccountSerializerRegistr
    lookup_fields = 'id'
    #lookup_url_kwargs = 'username'


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
         
        id = create_account_number()
        serializer.save(id=id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class AccountUpdate(generics.UpdateAPIView, generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_fields = 'id'
    def get_queryset(self):
        queryset = Account.objects.filter(id=self.kwargs['pk'])
        return queryset

class AccountDetail(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_fields = 'usernameid'

    def get_queryset(self):
        return self.queryset.filter(
            usernameid=self.kwargs['usernameid'])

    

class AccountDestroy(generics.DestroyAPIView, generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_fields = 'id'

    def get_queryset(self):
        queryset = Account.objects.filter(id=self.kwargs['pk'])
        return queryset
    

'''
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except IntegrityError as e:
            return Response("Нельзя удалить клиента с привязхаными счетами", status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def perform_destroy(self, instance):
        instance.delete()      
'''