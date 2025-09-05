from django.db import models
from django.contrib.auth.models import User



class Agent(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True)
    name= models.CharField(max_length=100)
    email = models.EmailField()
    contacts=models.CharField(max_length=20)
    profilepic= models.ImageField(upload_to='uploads/agentprofiles/',default=1)
    description=models.TextField(max_length =500)
    imageID= models.ImageField(upload_to='uploads/agents/',default=1)

    def __str__(self):
         return self.name


class Type(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
         return self.name



class Property(models.Model):
    name= models.CharField(max_length=100)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null = True, blank = True)
    price= models.FloatField(null = True)
    type= models.ForeignKey(Type,on_delete=models.CASCADE,default=1)
    picture= models.ImageField(upload_to='uploads/properties/',default=1)
    description= models.TextField(max_length =2000)
    upload_date = models.DateField(auto_now_add=True) 

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.picture.url
        except:
            url = ''
        return url
    

class Client(models.Model): 
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True)
    name= models.CharField(max_length=100)
    email = models.EmailField()

