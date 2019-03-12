from rest_framework import viewsets
from rest_framework import mixins
from .models import UserFav
from .serializers import UserFavSerializer


class UserFavViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    '''
    用户收藏
    '''
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
