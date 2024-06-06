from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination,CursorPagination

#all these paginations work only for genericviews or viewsets i.e Pagination is only performed automatically if you're using the generic views or viewsets



class WatchListPagination(PageNumberPagination):#this total is pagenumber pagination
    page_size=10  #will get 10 items per page i.e in postman the link will be like localhost:8000//watch/list/?page=2
    page_query_param='p' #here we are changing name i.e we will get localhost:8000//watch/list/?p=2
    page_size_query_param='size' #if user wants to channge page_size he can i.e in url he want to specify size=10 i.e localhost:8000//watch/list/?size=10
    max_page_size=10 #max you will get 10 elements per page even if user pass 100
    #if u need to go to last page you need to give localhost:8000//watch/list/?page=last
    last_page_strings='end' #if user wants to go to last page you need to give localhost:8000//watch/list/?page=end
    
    
#in LimitOffsetPagination  limit indicates the maximum number of items to return, and is equivalent to the page_size
#offset indicates for ex if we give limit=10 and offset=3 then it will return 10 items after 3 item i.e 4-13

class WatchListLOPagination(LimitOffsetPagination):
    default_limit=5 
    max_limit=10
    limit_query_param='limit'
    offset_query_param='start'#innstead of offset name we can give start i.e localhost:8000//watch/list/?limit=5&start=3
    
    
#in cursor pagination has only previous and next there is no like page=2 like pagenumberpagination in cursor pagination you dont have directly access to last page you need to click next next

class WatchListCPagination(CursorPagination):#
    page_size=5#in cursor pagination odering is there i.e it will oder items according latest time i.e created field in models.py
    ordering='created' #by default it is descending to ascending order i.e minus(-created) if you need reverswe i.e old to new you need to give created
    cursor_query_param='record' #insted of cursor we will get record as parameter in url link 
    