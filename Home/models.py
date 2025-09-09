from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator




class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contacts = models.CharField(max_length=20)
    profilepic = models.ImageField(upload_to='uploads/agentprofiles/', null=True, blank=True)
    description = models.TextField(max_length=500)
    imageID = models.ImageField(upload_to='uploads/agents/', null=True, blank=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
         return self.name


class Property(models.Model):
    name = models.CharField(max_length=100)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True, blank=True)
    price = models.FloatField(null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, default=1)
    
    picture= models.ImageField(upload_to='uploads/properties/',default=1)
    
    description = models.TextField(max_length=2000)
    size = models.FloatField(null=True)
    bedrooms = models.FloatField(null=True)
    bathrooms = models.FloatField(null=True)
    location = models.CharField(max_length=100, default='location')
    selrent = models.CharField(max_length=50,default='rent/sell')
    
    nav_video = models.FileField(
        upload_to="uploads/properties/videos/",
        null=True,
        blank=True
    )
   
    
    def __str__(self):
        return self.name + ' '+ self.location
    


# class PropertyDetail(models.Model):
#     name = models.CharField(max_length=100)
#     property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True)
#     price = models.FloatField(null=True)
#     type = models.ForeignKey(Type, on_delete=models.CASCADE, default=1)
    
#     picture= models.ImageField(upload_to='uploads/properties/',default=1)
    
#     description = models.TextField(max_length=2000)
#     size = models.FloatField(null=True)
#     bedrooms = models.FloatField(null=True)
#     bathrooms = models.FloatField(null=True)
#     location = models.CharField(max_length=100, default='location')
#     selrent = models.CharField(max_length=50,default='rent/sell')
    
#     nav_video = models.FileField(
#         upload_to="uploads/properties/videos/",
#         null=True,
#         blank=True
#     )
   
    
#     def __str__(self):
#         return self.name + ' '+ self.location  


class PropertyAlbum(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="album")
    image = models.ImageField(upload_to="uploads/properties/album/")

def __str__(self):
        return f"Album image {self.id} for {self.property.name}"

    

 # nav_video = models.FileField(
    #     upload_to="videos/",
    #     validators=[FileExtensionValidator(allowed_extensions=["mp4", "avi", "mov", "mkv"])],
    #     null=True,
    #     blank=True
    # )


# class Client(models.Model): 
#     user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True)
#     name= models.CharField(max_length=100)
#     email = models.EmailField()

