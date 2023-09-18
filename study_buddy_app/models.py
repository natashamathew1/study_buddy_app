from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.dispatch import receiver #add this
from django.db.models.signals import post_save #add this
from django.template.defaultfilters import slugify  # new

class Room(models.Model):
    name = models.CharField(max_length=1000)
class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)

class Class(models.Model):
    subject = models.CharField(max_length=4)
    catalog_number = models.CharField(max_length=4)
    course_section = models.CharField(max_length=3)
    def __str__(self):
        return self.subject + " " + self.catalog_number + " -- Section " + self.course_section

class Profile(models.Model):  # add this class and the following fields
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classes = models.ManyToManyField(Class)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = self.user.username
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)

    @receiver(post_save, sender=User)  # add this
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)  # add this
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Friends1(models.Model):
    users1 = models.ManyToManyField(User, null=True)
    current_user = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE,null=True)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend,create=cls.objects.get_or_create(current_user=current_user)
        friend.users1.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, create = cls.objects.get_or_create(current_user=current_user)
        friend.users1.remove(new_friend)


class FriendRequest(models.Model):
    sender=models.ForeignKey(User,null=True,related_name='sender1',on_delete=models.CASCADE)
    receiver=models.ForeignKey(User,null=True,on_delete=models.CASCADE)

##class User(AbstractUser):
##    friends = models.ManyToManyField("User", blank=True)
##
##class Friend_Request(models.Model):
##    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
##    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
##

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    users = models.ManyToManyField(User)
    def __str__(self):
        return str(self.title)+" "+str(self.start_time)+" "+str(self.end_time)
