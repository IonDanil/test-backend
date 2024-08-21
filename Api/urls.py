from django.urls import include, path

app_name = 'Api'

urlpatterns = [
    path('Api/v1/', include('Api.v1.urls')),
]
