from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserProfile(AbstractUser):
    """
    用户
    """
    GENDER_CHOICES = (
        ("male", u"男"),
        ("female", u"女")
    )
    name = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name=u"出生年月")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default=u"female", verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name=u"电话")
    email = models.EmailField(max_length=128, null=True, blank=True, verbose_name=u"邮箱")

    class Meta:
        verbose_name = u"用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=32, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
