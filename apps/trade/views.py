from rest_framework import mixins
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions
from rest_framework import viewsets
from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShoppingCartSerializers, ShoppingCartDetailSerializers
from .models import ShoppingCart


class ShoppingCartViewset(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ShoppingCartSerializers
    lookup_field = 'goods_id'

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ShoppingCartDetailSerializers
        else:
            return ShoppingCartSerializers
