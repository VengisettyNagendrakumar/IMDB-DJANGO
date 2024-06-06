from django.urls import path,include
from imdb_app.api.views import ReviewCreate, ReviewDetails, StreamPlatformDetailAv, StreamPlatformVS, UserReview, WatchDetailAv, StreamPlatformAV,WatchListAV,ReviewList,WatchListGV
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('stream',StreamPlatformVS,basename='streamplatform')
urlpatterns = [
   
    path('list/',WatchListAV.as_view(),name="movie_list"), 
    path('<int:pk>/',WatchDetailAv.as_view(),name="movie_details") ,
    path('list2/',WatchListGV.as_view(),name="watch-list") ,
    path('',include(router.urls)), #here b using viewsets and routers we can directly access stream list and access accodring to od we dont need to create 2 paths so for that i have commented below 2 paths i.epath('stream/<int:pk>',StreamPlatformDetailAv.as_view(),name="stream_details") ,path('stream/',StreamPlatformAV.as_view(),name="stream"),
    #  path('stream/<int:pk>',StreamPlatformDetailAv.as_view(),name="stream_details") ,
    # path('stream/',StreamPlatformAV.as_view(),name="stream-list"),
    # path('review/',ReviewList.as_view(),name="review"),
    # path('review/<int:pk>',ReviewDetails.as_view(),name="review_details")
    # path('stream/<int:pk>/review',ReviewList.as_view(),name="review_list"),#getting reviews for particular movie according to id here id indicates movie
    # path('stream/review/<int:pk>',ReviewDetails.as_view(),name="review_details"),
     path('<int:pk>/reviews/',ReviewList.as_view(),name="review_list"),#getting reviews for particular movie according to id here id indicates movie
      path('<int:pk>/review-create/',ReviewCreate.as_view(),name="review_create"), #creating new review for particular movie
       path('review/<int:pk>/',ReviewDetails.as_view(),name="review_details"),
       path('reviews/<str:username>/',UserReview.as_view(),name="user_review-detail"),
        #path('reviews/',UserReview.as_view(),name="user_review-detail"),this is url for when we use params in url i.e hhttp://127.0.0.1.8000/watch/reviews/?username=nagendra
    #     return Review.objects.filter(review_user__username=username)
    
]
