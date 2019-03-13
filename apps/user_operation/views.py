from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import authentication
from .models import UserFav, UserLeavingMessage,UserAddress
from .serializers import UserFavSerializer, UserFavDetialSerializer, UserLeavingMessageSerializr,UserAddressSerializer
from utils.permissions import IsOwnerOrReadOnly
from utils import permissions


class UserFavViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    '''
    用户收藏
    '''
    queryset = UserFav.objects.all()
    # serializer_class = UserFavSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsOwnerOrReadOnly,)
    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetialSerializer
        elif self.action == "create":
            return UserFavSerializer
        return UserFavSerializer

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)


class UserLeavingMessageViewset(viewsets.ModelViewSet):
    serializer_class = UserLeavingMessageSerializr
    authentication_classes = [JSONWebTokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [IsAuthenticated,permissions.IsOwnerOrReadOnly,]

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class UserAddressViewset(viewsets.ModelViewSet):
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated,permissions.IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication, authentication.SessionAuthentication]

    # def perform_destroy(self, instance):
    #     instance.isDelete = True
    #     instance.save()


    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
