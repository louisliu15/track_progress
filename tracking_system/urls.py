from rest_framework import routers
from .views import ListViewset, LoginViewset, ProcessViewset
from django.conf.urls import url, include
from rest_framework.authtoken import views as rest_framework_views

router = routers.DefaultRouter()
# get_user_info = LoginViewset.as_view({'get':'get_user_info'})

# router.register(r'users', UserViewset)
router.register(r'list', ListViewset)
router.register(r'process', ProcessViewset)
router.register(r'login', LoginViewset, 'login')

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
]
