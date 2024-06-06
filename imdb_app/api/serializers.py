from imdb_app.models import Review, StreamPlatform, WatchList
from rest_framework import serializers


#writing model serializers in model serializers we have default validation rules and default create and update methodsa are there

class ReviewSerializer(serializers.ModelSerializer):
    #Django's StringRelatedField automatically follows the foreign key relationship (review_user in this case), fetches the related object (User instance), and then returns a string representation of that object. Since you've specified read_only=True, this field will not be used for deserialization (i.e., input), only for serialization (i.e., output).
    review_user=serializers.StringRelatedField(read_only=True)#to get which review is submitted by which user i.e if we not give this we will get id if we give this we will get name
    class Meta:
        model=Review
        exclude=('watchlist',)
        #fields="__all__"  
class WatchListSerializer(serializers.ModelSerializer): #here movie is model name
    reviews=ReviewSerializer(many=True,read_only=True)#there are many reviews so we need to write many=true
    paltform=serializers.CharField(source='paltform.name')#we will get platform name here we can aslo wrte source paltform__name i.e platform name is foreign key in watchlist but that foreign key becomes id filed in straem platfoem model so we we write platform__ it jumps to streamplatform table access name 
    class Meta:
        model=WatchList
        fields="__all__"
        #exclude=['name']
class StreamPlatformSerializer(serializers.ModelSerializer):
    #here watchlist is related name in model
    watchlist=WatchListSerializer(many=True,read_only=True)#here one platform can have many movies here we are giving relationships if suppose netflix it shows all the movies netflix has
    #watchlist=serializers.StringRelatedField(many=True) #returns only the stribg related fields i.e we have to return that in model like this def __str__(self): return self.title 
    #watchlist=serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    #watchlist=serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name="movie_details")#here movie_details is name given in urls.py
    class Meta:
        model=StreamPlatform
        fields="__all__"
    