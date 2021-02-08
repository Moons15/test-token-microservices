from django.conf.urls import url
from .views import *

app_name = 'account'
urlpatterns = [
    url(r'^register/$', CreateUserAPIView.as_view()),
    url(r'^user/retrieve/$', RetrieveUserAPIView.as_view()),
    url(r'^send-email/$', EmailContactAPIView.as_view()),
    url(r'^login/$', LoginAPIView.as_view()),
]
