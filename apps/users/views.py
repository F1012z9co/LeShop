from random import choice
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework_jwt.settings import api_settings
from .serializers import SmsSerializer, UserRegSerializer, UserDetialSerializer
from utils.yunpian import YunPian
from utils.permissions import IsOwnerOrReadOnly
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


class UserViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    # serializer_class = UserRegSerializer
    queryset = UserProfile.objects.all()

    def get_object(self):
        return self.request.user

    def get_permissions(self):
        if self.action == "create":
            return []
        elif self.action == "retrieve":
            return [permissions.IsAuthenticated(), ]
        else:
            return [permissions.IsAuthenticated(), ]

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegSerializer
        elif self.action == "retrieve":
            return UserDetialSerializer
        else:
            return UserDetialSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)
        ret_dict = serializer.data

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        ret_dict["token"] = token
        ret_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(ret_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
