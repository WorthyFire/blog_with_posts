from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def can_delete(self, user):
        return user == self.user
    can_delete.admin_order_field = 'pub_date'
    can_delete.boolean = True
    can_delete.short_description = 'Можно удалить'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    image = models.ImageField(upload_to='comment_images/', null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def can_delete(self, user):
        return user == self.user

    def can_edit(self, user):
        return user == self.user