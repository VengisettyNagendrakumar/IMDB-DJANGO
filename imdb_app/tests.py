from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from imdb_app.api import serializers
from imdb_app import models

class StreamPlatformTestCase(APITestCase):
   #in stream_platform view we have permission as isadminor readonly so to create platform we need to login first and loggeduser must be admin  
    def setUp(self):
        self.user=User.objects.create_user(username="example",password="password@123")#to login we have create user first
        self.token=Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)#now here we logged in as a user
        
        self.stream=models.StreamPlatform.objects.create(name="Netflix",about="good platform",website="http://netflix.com")
    def test_streamplatform_create(self):
        data={
            "name":"Netflix",
            "about": "good platform",
            "website": "https://netflix.com"
        }
        response = self.client.post(reverse('streamplatform-list'), data) #streamplatform is basename used in default router if u need list use streamplatform-list if you need details use streamplatform-details
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN) #i.e for admin only we need response as HTTP_201_CREATED here we loged in as noraml user so we need HTTP_403_FORBIDDEN
    
    def test_streamplatform_list(self):
        response=self.client.get(reverse('streamplatform-list'))#this list is empty i.e we didmt logged in as a admin so we havent crreated any platform but above we are creating platform manually to access individual element in list        self.stream=models.StreamPlatform.objects.create(name="Netflix",about="good platform",website="http://netflix.com")

        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_streamplatform_ind(self):
        response=self.client.get(reverse('streamplatform-detail',args=(self.stream.id,)))#to access indidbidual list we need id 


class WatchListTestCase(APITestCase):
    
    
    def setUp(self):
        self.user=User.objects.create_user(username="example",password="password@123")#to login we have create user first
        self.token=Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)#now here we logged in as a user
        
        self.stream=models.StreamPlatform.objects.create(name="Netflix",about="good platform",website="http://netflix.com")
        self.watchlist=models.WatchList.objects.create(paltform=self.stream,title="example movie",storyline="good",active=True)#creating movie manually to access individual list
    def test_streamplatform_create(self):
        data={#to give platform we need to create platform fisrt i.e platform in watchlis is foreign key to stream platform 
            "paltform":self.stream,
            "title":"exmaple movie",
            "storyline":"Example storyline",
            "active":True
        }
        response = self.client.post(reverse('movie_list'), data) 
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN) #i.e for admin only we need response as HTTP_201_CREATED here we loged in as noraml user so we need HTTP_403_FORBIDDEN
    
    def test_watchlist_list_(self):
          response=self.client.get(reverse('movie_list'))
          self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_watchlist_ind(self):
        response=self.client.get(reverse('movie_details',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(),1)#we have count currently 1 i.e we have created only one movie so we can match with count also
        self.assertEqual(models.WatchList.objects.get().title, 'example movie')#we can match with title aslo

class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(username="example",password="password@123")#to login we have create user first
        self.token=Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream=models.StreamPlatform.objects.create(name="Netflix",about="good platform",website="http://netflix.com")#to create a review we need movie to create a movie we need platformso we created manually
        self.watchlist=models.WatchList.objects.create(paltform=self.stream,title="example movie",storyline="good",active=True)#creating movie manually to access individual list
        self.watchlist2=models.WatchList.objects.create(paltform=self.stream,title="example movie2",storyline="nice",active=True)#already  we gave review for example movie in post  so we are creating review again manually in below line so error occurs so to avoid that we are creating another movie
        self.review=models.Review.objects.create(review_user=self.user,rating=5,description="goodmovie",watchlist=self.watchlist2,active=True)#for updating review we need review id so we are manually creating review for that so id will be automaticallygenerated when we added review manually 
    #adding review as authenticated user
    def test_review_create(self):
        data={
            "review_user":self.user,
            "rating":4,
            "description":"good",
            "watchlist":"self.watchlist",
            "active":True
        }
        response=self.client.post(reverse('review_create',args=(self.watchlist.id,)),data)#for creating review we need movie i.e in urls <int:pk>/review-create is therre pk is movie id so we pass id here
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(),2)#we have count currently 2 i.e we have created only one review manually  and another one in test_create_review method
        response=self.client.post(reverse('review_create',args=(self.watchlist.id,)),data)#creating a review for 2 time by same user for same movie so we added restriction in views only one user can write one review so this will raise error so comment these lines or change http_response to 400
        self.assertEqual(response.status_code,status.HTTP_429_TOO_MANY_REQUESTS)
   
   
    #adding review as unauthenticated user 
    
    def test_create_unauthenticated(self):
        data={
            "review_user":self.user,
            "rating":4,
            "description":"good",
            "watchlist":"self.watchlist",
            "active":True
        }
        self.client.force_authenticate(user=None,token=None)#heere we are force authenticate i.e already we lged in one user above so we are force_authenticating making user as none user as none means we are not authenticated
        response=self.client.post(reverse('review_create',args=(self.watchlist.id,)),data)#postibg review without authentication so will get error so change http response
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    #updating a review
    def test_review_update(self):
        data={
            "review_user":self.user,
            "rating":5,
            "description":"updated",
            "watchlist":"self.watchlist",
            "active":False
        }
        response=self.client.put(reverse('review_details',args=(self.review.id,)),data)#creating a review for 2 time by same user for same movie so we added restriction in views only one user can write one review so this will raise error so comment these lines or change http_response to 400
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    #accessing review
    def test_review_list(self):
        response=self.client.get(reverse('review_list',args=(self.watchlist.id,)))#accesing review acc to movie id
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    #accessing individual review
    def test_review_ind(self):
        response=self.client.get(reverse('review_details',args=(self.review.id,)))#accesing individual review acc to review id
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    def test_review_user(self):
        response=self.client.get(reverse('user_review-detail',args=(self.user.username,)))
        #response=self.client.get('/watch/reviews/?username' + self.user.username)#accesing review through name check urls there is        path('reviews/<str:username>/',UserReview.as_view(),name="user_review-detail"),
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        
