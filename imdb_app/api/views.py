from django.shortcuts import get_object_or_404
from imdb_app.api.pagination import WatchListPagination,WatchListLOPagination,WatchListCPagination
from imdb_app.api.serializers import  ReviewSerializer, WatchListSerializer,StreamPlatformSerializer
from imdb_app.models import Review, WatchList,StreamPlatform
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status
from  rest_framework.views import APIView #to write class based views we need to use Apiview  
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from imdb_app.api.permissions import AdminOrReadOnly,ReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
from imdb_app.api.throttling import ReviewCreateThrottle,ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters #used for serach based filtering

class UserReview(generics.ListAPIView):#performing filtering through get_queryset 
    serializer_class = ReviewSerializer
    def get_queryset(self):
        username=self.kwargs['username']#current user i.e passing name given in urls
        return Review.objects.filter(review_user__username=username)#go to foreignkey first i.e review user and goto match usernme and returns it
     #i.e if name nagendra given while urls then uername will be nagendra and filter through get_queryset i.e which reviews are there under nagendra
     
    # def get_queryset(self):
    #     username=self.request.query_params.get('username',None)#this is also same like above but we want give in url i.e username=nagendra like this i.e hhttp://127.0.0.1.8000/watch/reviews/?username=nagendra
    #     return Review.objects.filter(review_user__username=username)








# we commented viewset below class i.e StreamPlatformVS to use modelviewset it is very simple in wich we dont need to write method for create,get etc
class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes=[AdminOrReadOnly]#admin can edit or else other read only 
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer #these model viewset has all methods create,get,put,patch,delete
         



# class StreamPlatformVS(viewsets.ViewSet): #check explanation in urls.py
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(user)
#         return Response(serializer.data)
#     def create(self, request):
#         serializer=StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        

class ReviewCreate(generics.CreateAPIView):#creating new review for particular movie
    permission_classes = [IsAuthenticated]
    throttle_classes=[ReviewCreateThrottle]
    def get_queryset(self):
        return Review.objects.all()
    serializer_class = ReviewSerializer
    def perform_create(self,serializer):#overriding create we use perform create we are overriding create because we are creating a new review according to particular movie this is deafult method so we have to write like this only i.e we need to add serializer in params
        pk=self.kwargs.get('pk')#in generics all methods are presnt so we are using get 
        movie=WatchList.objects.get(pk=pk)#getting that movie first
        user=self.request.user#get the user
        review_queryset=Review.objects.filter(watchlist=movie,review_user=user)#getting that movie and user
        if review_queryset.exists():
            raise ValidationError("Review already exists")#one user can submit one review for one movie
        if movie.number_rating == 0:#i.e no body given review and above we have saved the movie details acc to id in variable name called movie so we are using here
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating=( movie.avg_rating+serializer.validated_data['rating'])/2 #i.e old reviews+new review/2 i.e averag
        movie.number_rating=movie.number_rating+1 #to see no.of ratings
        movie.save()
        serializer.save(watchlist=movie,review_user=user)#to save to want to give which user is giving review we have to save that also to get error if he submit again
  
  
    
#now we are using concrete view class i.e generic view class in which we dont need to write anything it has less code than mixins
class ReviewList(generics.ListAPIView):#viewing review for particular movie 
    permission_classes = [IsAuthenticated]#if login only we can seee details
    serializer_class = ReviewSerializer
    throttle_classes=[ReviewListThrottle,AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]#filering can only applied for generic classes not for Apiview class
    filterset_fields = ['review_user__username', 'active']#i.e we are filtering based on this fields while doing we need to give like this hhttp://127.0.0.1.8000/watch/reviews/?review_user__username=nagendra or inple of username active=true or active=false or both using & hhttp://127.0.0.1.8000/watch/reviews/?review_user__username=nagendra & active=true
    def get_queryset(self):
        pk=self.kwargs['pk'] #getting review acc to movie id i.e for particular movie we are viewing review
        return Review.objects.filter(watchlist=pk) #here watchlist is is related name inn models.py here inplace of watchlist we can write anything



class ReviewDetails(generics.RetrieveUpdateDestroyAPIView): #by using this  one func we can get by id and we can get all reviews but for ListApiview used in above func if we need specific id detail we need to write code
    #permission_classes = [IsAuthenticatedOrReadOnly]#if login only we can update details if not we can just read the details
    #permission_classes=[AdminOrReadOnly]#using custom permissions written in permissions.py
    permission_classes=[ReviewUserOrReadOnly]
    #throttle_classes=[UserRateThrottle,AnonRateThrottle]#resctricting review details for all users for registered and unregistered no of requests are mentioned in settings.py
    #throttle_classes=[ReviewListThrottle,AnonRateThrottle]
    throttle_classes=[ScopedRateThrottle]
    throttle_scope='review-detail'#we have to give directly for scopedrate throttling like we given in throttling.py for each class
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer







# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all() #by using mixin we dont need to write methods explacitly for get ,post like written using APIView
#     serializer_class = ReviewSerializer #HERE listmodemixin used for get method and create model mixin used for post method
#     #here queryset is and serializer_class is default names we cant change them
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
# class ReviewDetails(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     serializer_class = ReviewSerializer
#     def get_queryset(self): #here we are overridng queryset method to retreive according to id 
#         return Review.objects.filter(id=self.kwargs['pk'])
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
class StreamPlatformAV(APIView):
    permission_classes=[AdminOrReadOnly]#admin can edit or else read only 
    def get(self,request):
        platform=StreamPlatform.objects.all()
        serializer=StreamPlatformSerializer(platform,many=True)#here we need to add after many=true context={'request':request} this is needed when we use the hperlinkedfield in serializer.py i.e watchlist=serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name="movie_details")
        return Response(serializer.data)
    def post(self,request):
        serializer=StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
class StreamPlatformDetailAv(APIView):
    permission_classes=[AdminOrReadOnly]
    def get(self, request,pk):
        try:
            movie=StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error':'not found'},status=status.HTTP_404_NOT_FOUND)
        serializer=StreamPlatformSerializer(movie)
        return Response(serializer.data)#serilalizer converts automatiacally into json format
    def put(self, request, pk):
        movie=StreamPlatform.objects.get(pk=pk)
        serializer=StreamPlatformSerializer(movie,data=request.data) 
        if serializer.is_valid(): #when came to here it check all vlidations written in serializers.py
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    def delete(self, request,pk):
        movie=StreamPlatform.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  


class WatchListGV(generics.ListAPIView):
    queryset=WatchList.objects.all()
    serializer_class=WatchListSerializer
    #pagination_class=WatchListPagination
    #pagination_class=WatchListLOPagination
    pagination_class=WatchListCPagination #when using cursor pagination we need comment all the filter_backends we used because cursor pagination filter items according to timestamp i.e new to old so if you give filter class again it will get error
    
    # filter_backends = [filters.SearchFilter]
    # search_fields=['title','paltform__name']#i.e in Stremplatformserializer is connected to watch list through foreign key in models so here search fisrt based on platform id and then it goes streamplatform and see matching platform name according to id 
    # #i.e hhttp://127.0.0.1.8000/watch/list2/?search=netflix
    
#   ^	istartswith	Starts-with search. i.e filterset_fields=['^title']  hhttp://127.0.0.1.8000/watch/list2/?search=n i.e gets all with starts with n
# =	iexact	Exact matches.
# $	iregex	Regex search.
# @	search	Full-text search (Currently only supported Django's PostgreSQL backend).
# None	icontains	Contains search (Default).
    filter_backends = [filters.OrderingFilter]#i.e acc to oder i.e ascending or descending
    ordering_fields = ['avg_rating']#hhttp://127.0.0.1.8000/watch/list2/?odering=avg_rating if u need descending to acending use minus(-) oreding=-avg_rating if u need descending
     
    
    
     
class WatchListAV(APIView): #class based views are in apiview so we are inhering 
    permission_classes=[AdminOrReadOnly]
    def get(self, request): #in classs based we can directly write funs we dont need to write if method==get like that
        movie=WatchList.objects.all()
        serializer=WatchListSerializer(movie,many=True)
        return Response(serializer.data)#serilalizer converts automatiacally into json format
        
    def post(self, request):
        serializer=WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
class WatchDetailAv(APIView):
    permission_classes=[AdminOrReadOnly]
    def get(self, request,pk):
        try:
            movie=WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error':'not found'},status=status.HTTP_404_NOT_FOUND)
        serializer=WatchListSerializer(movie)
        return Response(serializer.data)#serilalizer converts automatiacally into json format
    def put(self, request, pk):
        movie=WatchList.objects.get(pk=pk)
        serializer=WatchListSerializer(movie,data=request.data)
        if serializer.is_valid(): #when came to here it check all vlidations written in serializers.py
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    def delete(self, request,pk):
        movie=WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)       
    




