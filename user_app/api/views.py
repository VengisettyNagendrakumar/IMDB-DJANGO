from rest_framework.authtoken.models import Token #autogenerate token when registered check code snippet in models
from rest_framework.decorators import api_view
#from rest_framework_simplejwt.tokens import RefreshToken #to create token manually 

from user_app.api.serializers import RegistrationSerializer
from rest_framework.response import Response
from user_app import models #we are importing models beacuse when user is registered models must be called because token generaing code is in models
from rest_framework import status


@api_view(['POST'])
def logout_view(request):
    if request.method=='POST':#we give give post request in postman then only we are deleting the token
        request.user.auth_token.delete()#requset.user means currently logged in user and if he logout we are destroying the token
        return Response(status=status.HTTP_200_OK)






@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST': #in registationserializer we use model serializer so in model serializer we have methods like get,post  like that so we wrote if condition here
        serializer = RegistrationSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()
            data['response']="Registration successful"
            data['username']=account.username
            data['email']=account.email
            token=Token.objects.get(user=account).key#getting token acc to user
            data['token']=token
            # refresh = RefreshToken.for_user(account) #we will get token automatically when registered this is jwt authentication
            # data['token']={
            #                  'refresh': str(refresh),
            #                 'access': str(refresh.access_token),
            #             }
            
        else:
            data=serializer.errors
            
        return Response(data,status=status.HTTP_201_CREATED)