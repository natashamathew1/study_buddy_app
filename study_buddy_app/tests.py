from django.contrib.auth.models import User
from django.test import TestCase
from .models import Profile, Class
from django.dispatch import receiver 
from django.db.models.signals import post_save
from django.db import models
from .forms import UserForm
from .views import user
from study_buddy_app.models import Room, Message
from .models import Friends1
from .models import FriendRequest
from django.contrib.auth import get_user_model
from django.db.models import Q # new

class UserModelTests(TestCase):
    def test_user_created(self):
        #ejriejfoei
        """
        exists() returns True when a user was successfully created
        """
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.last_name = 'Lennon'
        user.save()
        self.assertIs(User.objects.filter(username='john').exists(), True)

class UserProfileTests(TestCase):
    def test_profile_created(self):
        new_user = User.objects.create_user('hello', 'what@hello.com', 'natpassword2')
        self.assertIs(Profile.objects.filter(user=new_user).exists(), True)
    def test_save_profile(self):
        new_user = User.objects.create_user('hello', 'what@hello.com', 'natpassword2')
        first_profile = Profile.objects.get(user=new_user)
        self.assertEqual(new_user.username, 'hello')
        new_user.username = 'nat'
        new_user.save()
        second_profile = Profile.objects.get(user=new_user)
        self.assertEqual(first_profile, second_profile)
        self.assertEqual(new_user.username, 'nat')
    def test_profile_str(self):
        new_user = User.objects.create_user('john', 'john@example.com', 'password123')
        john_profile = Profile.objects.get(user=new_user)
        self.assertEqual(str(john_profile), 'john')

class ChatTest(TestCase):
    def test_room_created(self):
        room = "this_is_a_test_room"
        new_room = Room.objects.create(name=room)
        new_room.save()
        self.assertIs(Room.objects.filter(name=room).exists(), True)
        
    def test_message_sent(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.last_name = 'Lennon'
        user.save()

        room = "this_is_a_test_room"
        new_room = Room.objects.create(name=room)
        new_room.save()

        new_message = Message.objects.create(value="hello world", user="john", room="this_is_a_test_room")
        new_message.save()
        self.assertIs(Message.objects.filter(value="hello world", user="john", room="this_is_a_test_room").exists(), True)

    # def test_blank_message(self):
    #     user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    #     user.last_name = 'Lennon'
    #     user.save()

    #     room = "this_is_a_test_room"
    #     new_room = Room.objects.create(name=room)
    #     new_room.save()

    #     fakeMessage = ""
    #     #this is what i do in view
    #     if fakeMessage:    
    #         new_message = Message.objects.create(value=fakeMessage, user="john", room="this_is_a_test_room")
    #         new_message.save()
    #     self.assertIs(Message.objects.filter(value="", user="john", room="this_is_a_test_room").exists(), False)
    #     self.assertIs(len(Message.objects.all()) == 0, True)


class FriendRequestTest(TestCase):
    def test_send_request(self):
        first_user = User.objects.create_user('me', 'me@example.com','mepassword')
        second_user = User.objects.create_user('you', 'you@example.com', 'youpassword')
        model = FriendRequest.objects.create(sender=first_user, receiver=second_user)
        self.assertIs(FriendRequest.objects.filter(sender=first_user,receiver=second_user).exists(), True)
    def test_friends(self):
        first_user = User.objects.create_user('me', 'me@example.com','mepassword')
        second_user = User.objects.create_user('you', 'you@example.com', 'youpassword')
        Friends1.make_friend(first_user, second_user)
        Friends1.make_friend(second_user, first_user)
        self.assertIs(Friends1.objects.filter(users1=first_user, current_user=second_user).exists(), True)
        self.assertIs(Friends1.objects.filter(users1=second_user, current_user=first_user).exists(), True)

class PublicProfileTests(TestCase):
    def test_public_profile(self):
        new_user = User.objects.create_user('Michael', 'Jackson@hehe.com', 'password123')
        profile = Profile.objects.get(user=new_user)
        self.assertEqual(new_user.username, profile.slug)

    def test_public_profile_change_username(self):
        new_user = User.objects.create_user('Michael', 'Jackson@hehe.com', 'password123')
        new_user.username = 'CHANGEEEEEE'
        new_user.save()
        profile = Profile.objects.get(user=new_user)
        self.assertEqual(new_user.username, profile.slug)

class ClassModelTests(TestCase):
    def test_class_created(self):
        new_class = Class(subject='CS', catalog_number='3240', course_section='002')
        new_class.save()
        self.assertIs(Class.objects.filter(catalog_number='3240').exists(), True)

    def test_class_str(self):
        new_class = Class(subject='CS', catalog_number='3240', course_section='002')
        new_class.save()
        self.assertEqual(str(new_class), 'CS 3240 -- Section 002')
        
class SearchFeatureTest(TestCase):
    def test_search_name1(self):
        new_user = User.objects.create_user('Michael', 'Jackson@hehe.com', 'password123')
        self.assertIs(len(User.objects.filter(Q(username__iexact="Michael")))==1, True)
    
    def test_search_name_none(self):
        self.assertIs(len(User.objects.filter(Q(username__iexact="John Doe")))==0, True)
    
    def test_search_name_lowercase(self):
        new_user = User.objects.create_user('Michael', 'Jackson@hehe.com', 'password123')
        self.assertIs(len(User.objects.filter(Q(username__iexact="michael")))==1, True)
        new_user.delete()
    
    def test_class_without_catalog_number(self):
        """Return all the users."""
        User = get_user_model()
        new_user = User.objects.create_user('Michael', 'Jackson@hehe.com', 'password123')
        new_user.save()
        new_user1 = User.objects.create_user('John', 'John@hehe.com', 'password1234')
        new_user1.save()
        new_user2 = User.objects.create_user('Jane', 'Jane@hehe.com', 'password12345')
        new_user2.save()
        new_class = Class()
        new_class.subject = "ITAL"
        new_class.catalog_number = "1000"
        new_class.course_section = "2"
        new_class.save()
        new_user.profile.classes.add(new_class)
        new_user1.profile.classes.add(new_class)
        new_user2.profile.classes.add(new_class)

        query = "ITAL"
        users = User.objects.filter(Q(username__iexact=query) | Q(username__iexact=query))
        def has_numbers(inputString):
            return any(char.isdigit() for char in inputString)
        flag1 = not query is None and not has_numbers(query)
        flag2 = not query is None and has_numbers(query)
        

        if flag1:
            users |= User.objects.filter(Q(profile__classes__subject__iexact=query))

        if flag2:
            arr = query.split()
            if len(arr) == 2:
                users |= User.objects.filter(Q(profile__classes__subject__iexact=arr[0]) & Q(profile__classes__catalog_number__iexact=arr[1]))
        users = users.distinct()
        
        self.assertIs((len(users))==3, True)
        new_user.delete()
        new_user1.delete()
        new_user2.delete()
        new_class.delete()

    def test_class_without_catalog_number_lowercase(self):
        """Return all the users."""
        User = get_user_model()
        new_user = User.objects.create_user('Michael', 'Jackson@hehe.com', 'password123')
        new_user.save()
        new_user1 = User.objects.create_user('John', 'John@hehe.com', 'password1234')
        new_user1.save()
        new_user2 = User.objects.create_user('Jane', 'Jane@hehe.com', 'password12345')
        new_user2.save()
        new_class = Class()
        new_class.subject = "ITAL"
        new_class.catalog_number = "1000"
        new_class.course_section = "2"
        new_class.save()
        new_user.profile.classes.add(new_class)
        new_user1.profile.classes.add(new_class)
        new_user2.profile.classes.add(new_class)

        query = "ital"
        users = User.objects.filter(Q(username__iexact=query) | Q(username__iexact=query))
        def has_numbers(inputString):
            return any(char.isdigit() for char in inputString)
        flag1 = not query is None and not has_numbers(query)
        flag2 = not query is None and has_numbers(query)
        

        if flag1:
            users |= User.objects.filter(Q(profile__classes__subject__iexact=query))

        if flag2:
            arr = query.split()
            if len(arr) == 2:
                users |= User.objects.filter(Q(profile__classes__subject__iexact=arr[0]) & Q(profile__classes__catalog_number__iexact=arr[1]))
        users = users.distinct()
        
        self.assertIs((len(users))==3, True)
        new_user.delete()
        new_user1.delete()
        new_user2.delete()
        new_class.delete()
    
    def test_class_without_catalog_number_non_existant(self):
        """Return all the users."""
        User = get_user_model()
        new_user = User.objects.create_user('Michael', 'Jackson@hehe.com', 'password123')
        new_user.save()
        new_user1 = User.objects.create_user('John', 'John@hehe.com', 'password1234')
        new_user1.save()
        new_user2 = User.objects.create_user('Jane', 'Jane@hehe.com', 'password12345')
        new_user2.save()
        new_class = Class()
        new_class.subject = "ITAL"
        new_class.catalog_number = "1000"
        new_class.course_section = "2"
        new_class.save()
        new_user.profile.classes.add(new_class)
        new_user1.profile.classes.add(new_class)
        new_user2.profile.classes.add(new_class)

        query = "itaz"
        users = User.objects.filter(Q(username__iexact=query) | Q(username__iexact=query))
        def has_numbers(inputString):
            return any(char.isdigit() for char in inputString)
        flag1 = not query is None and not has_numbers(query)
        flag2 = not query is None and has_numbers(query)
        

        if flag1:
            users |= User.objects.filter(Q(profile__classes__subject__iexact=query))

        if flag2:
            arr = query.split()
            if len(arr) == 2:
                users |= User.objects.filter(Q(profile__classes__subject__iexact=arr[0]) & Q(profile__classes__catalog_number__iexact=arr[1]))
        users = users.distinct()
        
        self.assertIs((len(users))==0, True)
        new_user.delete()
        new_user1.delete()
        new_user2.delete()
        new_class.delete()

    def test_class_with_catalog_number(self):
        """Return all the users."""
        User = get_user_model()
        new_user = User.objects.create_user('Michael', 'Jackson@hehe.com', 'password123')
        new_user.save()
        new_user1 = User.objects.create_user('John', 'John@hehe.com', 'password1234')
        new_user1.save()
        new_user2 = User.objects.create_user('Jane', 'Jane@hehe.com', 'password12345')
        new_user2.save()
        new_class = Class()
        new_class.subject = "ITAL"
        new_class.catalog_number = "1000"
        new_class.course_section = "2"
        new_class.save()
        new_user.profile.classes.add(new_class)
        new_user1.profile.classes.add(new_class)
        new_user2.profile.classes.add(new_class)

        query = "ITAL 1000"
        users = User.objects.filter(Q(username__iexact=query) | Q(username__iexact=query))
        def has_numbers(inputString):
            return any(char.isdigit() for char in inputString)
        flag1 = not query is None and not has_numbers(query)
        flag2 = not query is None and has_numbers(query)
        

        if flag1:
            users |= User.objects.filter(Q(profile__classes__subject__iexact=query))

        if flag2:
            arr = query.split()
            if len(arr) == 2:
                users |= User.objects.filter(Q(profile__classes__subject__iexact=arr[0]) & Q(profile__classes__catalog_number__iexact=arr[1]))
        users = users.distinct()
        
        self.assertIs((len(users))==3, True)
        new_user.delete()
        new_user1.delete()
        new_user2.delete()
        new_class.delete()
    def test_class_with_catalog_number_lowercase(self):
        """Return all the users."""
        User = get_user_model()
        new_user = User.objects.create_user('Michael', 'Jackson@hehe.com', 'password123')
        new_user.save()
        new_user1 = User.objects.create_user('John', 'John@hehe.com', 'password1234')
        new_user1.save()
        new_user2 = User.objects.create_user('Jane', 'Jane@hehe.com', 'password12345')
        new_user2.save()
        new_class = Class()
        new_class.subject = "ITAL"
        new_class.catalog_number = "1000"
        new_class.course_section = "2"
        new_class.save()
        new_user.profile.classes.add(new_class)
        new_user1.profile.classes.add(new_class)
        new_user2.profile.classes.add(new_class)

        query = "ital 1000"
        users = User.objects.filter(Q(username__iexact=query) | Q(username__iexact=query))
        def has_numbers(inputString):
            return any(char.isdigit() for char in inputString)
        flag1 = not query is None and not has_numbers(query)
        flag2 = not query is None and has_numbers(query)
        

        if flag1:
            users |= User.objects.filter(Q(profile__classes__subject__iexact=query))

        if flag2:
            arr = query.split()
            if len(arr) == 2:
                users |= User.objects.filter(Q(profile__classes__subject__iexact=arr[0]) & Q(profile__classes__catalog_number__iexact=arr[1]))
        users = users.distinct()
        
        self.assertIs((len(users))==3, True)
        new_user.delete()
        new_user1.delete()
        new_user2.delete()
        new_class.delete()
    
    def test_class_with_catalog_number_non_existant(self):
        """Return all the users."""
        User = get_user_model()
        new_user = User.objects.create_user('Michael', 'Jackson@hehe.com', 'password123')
        new_user.save()
        new_user1 = User.objects.create_user('John', 'John@hehe.com', 'password1234')
        new_user1.save()
        new_user2 = User.objects.create_user('Jane', 'Jane@hehe.com', 'password12345')
        new_user2.save()
        new_class = Class()
        new_class.subject = "ITAL"
        new_class.catalog_number = "1000"
        new_class.course_section = "2"
        new_class.save()
        new_user.profile.classes.add(new_class)
        new_user1.profile.classes.add(new_class)
        new_user2.profile.classes.add(new_class)

        query = "itaz 1000"
        users = User.objects.filter(Q(username__iexact=query) | Q(username__iexact=query))
        def has_numbers(inputString):
            return any(char.isdigit() for char in inputString)
        flag1 = not query is None and not has_numbers(query)
        flag2 = not query is None and has_numbers(query)
        

        if flag1:
            users |= User.objects.filter(Q(profile__classes__subject__iexact=query))

        if flag2:
            arr = query.split()
            if len(arr) == 2:
                users |= User.objects.filter(Q(profile__classes__subject__iexact=arr[0]) & Q(profile__classes__catalog_number__iexact=arr[1]))
        users = users.distinct()
        
        self.assertIs((len(users))==0, True)
        new_user.delete()
        new_user1.delete()
        new_user2.delete()
        new_class.delete()
