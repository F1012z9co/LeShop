from rest_framework import serializers
from .models import Goods
from .models import Goods, GoodsCategory, Banner, GoodsImage


class GoodsImagesSerialer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image",)


class GoodsSerializer(serializers.ModelSerializer):
    images = GoodsImagesSerialer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    """
    轮播图
    """

    class Meta:
        model = Banner
        fields = "__all__"
