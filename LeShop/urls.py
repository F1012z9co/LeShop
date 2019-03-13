from django.conf.urls import url, include
import xadmin
from django.views.static import serve
from LeShop.settings import MEDIA_ROOT
from rest_framework.routers import DefaultRouter

from goods.views import GoodsListViewSet, CategoryViewset, BannerViewset
from users.views import SmsCodeViewset, UserViewset
from user_operation.views import UserFavViewset, UserLeavingMessageViewset, UserAddressViewset
from trade.views import ShoppingCartViewset
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view
from rest_framework_jwt.views import obtain_jwt_token

# from django.contrib import admin

router = DefaultRouter()
router.register(r'goods', GoodsListViewSet, base_name='goods')
router.register(r'categorys', CategoryViewset, base_name="categorys")
router.register(r'banners', BannerViewset, base_name="banners")
router.register(r'code', SmsCodeViewset, base_name="code")
router.register(r'users', UserViewset, base_name="users")
router.register(r'userfavs', UserFavViewset, base_name="userfavs")
router.register(r'messages', UserLeavingMessageViewset, base_name="messages")
router.register(r'address', UserAddressViewset, base_name="address")
router.register(r'shopcarts', ShoppingCartViewset, base_name="shopcarts")


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url('xadmin/', xadmin.site.urls),
    url('ueditor', include('DjangoUeditor.urls')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    url(r'^login/', obtain_jwt_token),
    url(r'docs/', include_docs_urls(title='乐农客')),
    url(r'docs2/', get_swagger_view(title='乐农客'))

]
