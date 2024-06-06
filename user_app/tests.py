from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User#we are writing testcase for login ,logout,register so we used user model for that so we need to import

class RegisterTestCase(APITestCase):
    def test_register(self):#name always must starts from test_name
        data={ #here testing i.e sample data giving and posting and testing
            "username":"testcase",
            "email":"testcase@example.com",
            "password":"password@123",
            "password2":"password@123"
            
        }
        response=self.client.post(reverse('register'),data,format='json')#'register means name given in urls i.e name="register"
        self.assertEqual(response.status_code,status.HTTP_201_CREATED) #if this testcase response is equal to original response i.e written code for register post method then test case is successful i.e return Response(data,status=status.HTTP_201_CREATED) this is line present in register func in views.py
#this data will not save in database just using for testing purpose
class LoginLogoutTestCase(APITestCase):
    #for testing login or logout we need to create user first so we need to do that in setup function which is presnt in django setup function will be called first after testcase function is called
        #u thisnk that already we have registered one user in above class then why should we are creating new user for login so the data will not save in databse just its temporary if class is over it will be destroyed

    def setUp(self):
        self.user=User.objects.create_user(username="exmaple",password="password@123")#using user model here
    
        def test_login(self):
            data={
                "username":"exmaple",
                "password":"password@123"
            }
            response=self.client.post(reverse('login'),data,format='json')
            self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        def test_logout(self):
            self.token=Token.objects.get(user__username="exmaple")#to logout we need to have token i.e we addded token authentication
            #self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)  #here we are logging so we are already logged in for above userso no need to write this      
            response=self.client.post(reverse('logout'))
            self.assertEqual(response.status_code,status.HTTP_200_OK) 
'''In Django ORM, when you want to perform a lookup through a ForeignKey or a OneToOneField, you use double underscores (__) to traverse relationships between models.
In your case, since the Token model likely has a ForeignKey to the User model, you need to specify user__username to traverse this relationship and filter tokens based on the username of the associated user.
If you just use username, Django would interpret it as trying to filter tokens based on a field directly on the Token model named username, which doesn't exist, thus resulting in an error.
So, user__username is indeed the correct syntax to filter tokens based on the username of the associated user.
In the typical structure of Django authentication with tokens, the username field is present in the User model, not in the Token model.
The User model represents the user accounts in your system. It typically includes fields such as username, password, email, etc.
The Token model usually represents authentication tokens associated with users. It typically includes fields like key (the token itself) and a ForeignKey to the User model, representing which user the token belongs to.
So, when you use user__username in a query on the Token model, you are traversing the ForeignKey relationship from the Token model to the User model and then filtering based on the username field in the User model. This is the standard way to filter tokens based on the username of the associated user.'''





