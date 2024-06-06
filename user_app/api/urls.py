from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token#this give token if we send username and password


from user_app.api.views import logout_view, registration_view 
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)

 
urlpatterns = [
   path('login/',obtain_auth_token,name="login"),#if we login it will give token 
   path('register/',registration_view,name="register"),
    path('logout/',logout_view,name="logout"),
#      path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #these urls are by default for jwt authentication we do not change them and these generate token automatically 2 tokens one is access token and refresh token i.e shortterm,longterm token access token will be there only for 5 min to generate access token we use refresh tokenand refresh token valid for 24 hours and these tokens will not store in db system will vewrify automatically
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),#this token has 3 parts header,payload,signture after access token expires we need to use this url and refresh token to get another access token
# #the disadvantage of jwt token is we cant delete the token 
]


