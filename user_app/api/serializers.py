from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['username', 'email','password', 'password2']#3 fileds are already defined inUser model but we added extra field password2 we need to define it
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def save(self):#overriding save cause we need to check password1==password2 like this conditions
        password=self.validated_data['password']
        #In Django, self.validated_data is a dictionary-like object that holds the validated and cleaned data of a serializer in Django REST Framework. When you use self.validated_data['password'], you're accessing the value of the 'password' field from the validated data.
        password2=self.validated_data['password2']
        if password!=password2:
            raise serializers.ValidationError({'error':'p1 and p2 should be equal'})
        if User.objects.filter(email=self.validated_data['email']).exists():#our motive is email must be unique so we are getting email fromuser 
            raise serializers.ValidationError({'error':'email already exists'})
        
        account=User(email=self.validated_data['email'],username=self.validated_data['username']) #creating user manually
        account.set_password(password)
        account.save()
        return account