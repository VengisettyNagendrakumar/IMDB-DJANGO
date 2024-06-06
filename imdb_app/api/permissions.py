#writing custom permissions and can import when needed
from rest_framework import permissions
class AdminOrReadOnly(permissions.IsAdminUser):#if admin is logged he can edit details or if another logged just read only
    def has_permission(self, request, view): #this function is deafult we have to write like this only
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff) #i.e if user is staff user i.e admin
class ReviewUserOrReadOnly(permissions.BasePermission):#if user is review owner he can edit review or else just he can see the review
    def has_object_permission(self, request, view, obj):
        #safe method checks if the HTTP method of the request is one of the safe methods (GET, HEAD, OPTIONS). If the method is safe, it returns True, indicating that the user has permission to perform the action (such as viewing the review) regardless of the object's ownership.
        if request.method in permissions.SAFE_METHODS: #safe method means get only if get he can view the review
            return True
        else:#if method is put or destroy it comes here and check
            #here review_user is filed name given in models
            if obj.review_user == request.user or request.user.is_admin: #here request.user means logged in user and obj.review_user is owner of review
                return True
            else:
                return False
            #obj.review_user: This refers to the user who created the review, as retrieved from the Review object (obj). Since review_user is a foreign key field in the Review model that points to the User model, obj.review_user represents the actual User instance who created the review.

#request.user: This represents the user making the HTTP request. It's typically set by the authentication mechanism in your Django REST Framework setup.