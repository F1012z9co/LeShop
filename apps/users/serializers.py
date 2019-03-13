import re
from datetime import datetime, timedelta
from rest_framework.validators import UniqueValidator
from .models import VerifyCode
from rest_framework import serializers
from django.contrib.auth import get_user_model
from LeShop import settings

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, label="手机号", help_text="请输入手机号")

    def validate_mobile(self, mobile):

        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        if not re.match(settings.REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号不正确")

        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")
        return mobile


class UserDetialSerializer(serializers.ModelSerializer):
    """
    用户信息
    """

    class Meta:
        model = User
        fields = "__all__"


class UserRegSerializer(serializers.ModelSerializer):
    """
    注册
    """
    code = serializers.CharField(max_length=4, min_length=4, error_messages={
        "max_length": "验证码格式错误",
        "min_length": "验证码格式错误"
    }, label="验证码", write_only=True)

    username = serializers.CharField(
        label="用户名",
        validators=[UniqueValidator(queryset=User.objects.all(), message="用户已存在")]
    )

    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    def create(self, validated_data):
        user = super().create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if last_record.add_time >five_mintes_ago :
                raise serializers.ValidationError("验证码过期")
            print(last_record.code)
            if code != last_record.code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("请输入正确的验证码")

    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ("username", "mobile", "code", "password")
