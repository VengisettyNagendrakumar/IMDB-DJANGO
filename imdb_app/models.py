from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User #user id default table present in django
# Create your models here.
class StreamPlatform(models.Model):
    name=models.CharField(max_length=50)
    about=models.CharField(max_length=150)
    website=models.URLField(max_length=100)
    def __str__(self):
        return self.name
class WatchList(models.Model):
    title=models.CharField(max_length=50)
    storyline=models.CharField(max_length=200)
    paltform=models.ForeignKey(StreamPlatform,on_delete=models.CASCADE,related_name="watchlist")#one movie can have one platform but one platform can have multiple moovies so we need to use foreign keys i.e many to one for many platforms to one we use foreign keys
    active=models.BooleanField(default=True)
    avg_rating=models.FloatField(default=0)
    number_rating=models.IntegerField(default=0)#to see no. of ratings
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
class Review(models.Model):
    review_user=models.ForeignKey(User,on_delete=models.CASCADE)#to know which user is created the review
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description=models.CharField(max_length=200,null=True)
    active=models.BooleanField(default=True)#if active is false it is fake review 
    watchlist=models.ForeignKey(WatchList,on_delete=models.CASCADE,related_name="reviews")#one review can have one movie but one movie can have many reviews i.e many to one 
    created=models.DateTimeField(auto_now_add=True)#when we create a new movie time will be created
    update=models.DateTimeField(auto_now=True)#here auto_now i.e ever time we update time will be updated
    
    def __str__(self) :
        return str(self.rating) + "| "+self.watchlist.title + "|"+str(self.review_user) #this return will effect in admin page what we return that we can seen in admin


