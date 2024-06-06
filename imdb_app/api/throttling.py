from rest_framework.throttling import UserRateThrottle#giving restriction for loged in users


'''
Throttling in Django REST Framework is a mechanism used to limit the number of requests that a user can make to an API within a certain period of time. This is often done to prevent abuse of the API, ensure fair usage, and maintain server stability.

Django REST Framework provides built-in support for throttling. There are several built-in throttling classes you can use, such as:

AnonRateThrottle: Limits the rate of requests from unauthenticated users.
UserRateThrottle: Limits the rate of requests from authenticated users.
ScopedRateThrottle: Limits the rate of requests based on a specific scope, such as a specific endpoint or action.
'''
class ReviewCreateThrottle(UserRateThrottle):
    scope = 'review-create'#in place of review-create we can give any name
class ReviewListThrottle(UserRateThrottle):
    scope = 'review-list'
    
