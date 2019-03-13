from rest_framework import serializers
from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from rest_framework.validators import UniqueTogetherValidator
from goods.serializers import GoodsSerializer


class UserFavDetialSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = UserFav
        fields = "__all__"


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )]
        model = UserFav
        fields = ("user", "goods", 'id')


class UserLeavingMessageSerializr(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m%d %H:%M")

    class Meta:
        model = UserLeavingMessage
        fields = "__all__"


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m%d %H:%M")

    class Meta:
        model = UserAddress
        fields = "__all__"