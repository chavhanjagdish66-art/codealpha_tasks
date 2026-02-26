from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="dp",null=True,blank=True)
    followers = models.ManyToManyField(User,related_name="followers",blank=True)
    following = models.ManyToManyField(User,related_name="following",blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to="posts",null=True,blank=True)
    likes = models.ManyToManyField(User,blank=True,related_name="liked_posts")

    def __str__(self):
        return self.author.username


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)


@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)