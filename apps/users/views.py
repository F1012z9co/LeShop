from random import choice
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import SmsSerializer, UserRegSerializer
from utils.yunpian import YunPian
from LeShop import settings
from .models import VerifyCode, UserProfile


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SmsSerializer

    def generate_code(self):
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        yun_pian = YunPian(settings.APIKEY)
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code, mobile=serializer.validated_data["mobile"])
        if sms_status["code"] != 0:
            return Response(sms_status['msg'], status=status.HTTP_400_BAD_REQUEST)
        else:
            VerifyCode(code=code, mobile=serializer.validated_data["mobile"]).save()
            return Response(sms_status["msg"], status=status.HTTP_201_CREATED)


class UserViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserRegSerializer
    queryset = UserProfile.objects.all()
