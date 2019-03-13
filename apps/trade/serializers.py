from rest_framework import serializers
from .models import ShoppingCart
from goods.models import Goods
from goods.serializers import GoodsSerializer


class ShoppingCartDetailSerializers(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShoppingCartSerializers(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())
    nums = serializers.IntegerField(required=True, label="商品数量", min_value=1, error_messages={
        "required": "必须填写商品数量"
    })

    def create(self, validated_data):
        user = self.context["request"].user
        goods = validated_data["goods"]
        nums = validated_data["nums"]
        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            existed[0].nums += nums
            existed[0].save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        instance.nums += validated_data["nums"]
        instance.save()
        return instance