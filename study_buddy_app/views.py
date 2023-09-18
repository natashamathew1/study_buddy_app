from django.shortcuts import render, redirect, get_object_or_404
from study_buddy_app.models import Room, Message, Profile
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from django.db.models import Q # new
from django.views import generic
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.views import View

from django.shortcuts import render
import requests
from django import template

register = template.Library()
from .models import Profile, Class
from .forms import UserForm
from django import forms
from .models import Friends1
from .models import FriendRequest
#from .models import Class
from django.views import generic
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from allauth.socialaccount.models import SocialToken, SocialApp, SocialAccount

from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
from django.contrib import messages
from .models import *
from .utils import Calendar
from datetime import datetime
from pytz import timezone
from allauth.socialaccount.models import SocialAccount
import re
class SearchResultsView(generic.ListView):
    template_name = 'study_buddy_app/searchResults.html'
    context_object_name = 'search_results_list'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            template = loader.get_template('socialaccount/login.html')
            context = {}
            return redirect('/study_buddy_app/accounts/google/login/')
        return super(SearchResultsView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        """Return all the users."""
        query = self.request.GET.get("q")
        User = get_user_model()
        # search based on username
        users = User.objects.filter(Q(username__iexact=query) | Q(username__iexact=query))
        cardResults = []
        if not query or query is "":
            combination = zip(users, cardResults) 
            return {'combination': combination, 'user': self.request.user}
        #search based on first name
        users |= User.objects.filter(Q(first_name__iexact=query) | Q(first_name__iexact=query))

        # search based on last name only
        users |= User.objects.filter(Q(last_name__iexact=query) | Q(last_name__iexact=query))

        #search based on first and last name
        copy = query
        firstLastArr = copy.split(' ', 2)
        if len(firstLastArr) > 1: 
            users |= User.objects.filter(Q(first_name__iexact=firstLastArr[0]) & Q(last_name__iexact=firstLastArr[1]))


        # searcj based on class
        def has_numbers(inputString):
            return any(char.isdigit() for char in inputString)
        flag1 = not query is None and not has_numbers(query)
        flag2 = not query is None and has_numbers(query)
        flag3 = not query is None and has_numbers(query[0])

        if flag1:
            users |= User.objects.filter(Q(profile__classes__subject__iexact=query))

        if flag2 and not flag3:
            copy = query
            copy = copy.replace(" ", "")
            temp = re.compile("([a-zA-Z]+)([0-9]+)")
            arr = temp.match(copy).groups()
            if len(arr) == 2:
                users |= User.objects.filter(Q(profile__classes__subject__iexact=arr[0]) & Q(profile__classes__catalog_number__iexact=arr[1]))
        users = users.distinct()
        for user in users: 
            if flag1:
                cardResults.append(user.profile.classes.all().filter(Q(subject__iexact=query)))
            if flag2:
                cardResults.append(user.profile.classes.all().filter(Q(subject__iexact=arr[0]) & Q(catalog_number__iexact=arr[1])))
        combination = zip(users, cardResults)
        return {'combination': combination, 'user': self.request.user}
    
    


def index(request):
    template = loader.get_template('study_buddy_app/home.html')
    context = {}
    return HttpResponse(template.render(context, request))


def sign_in(request):
    template = loader.get_template('study_buddy_app/google_login.html')
    context = {}
    return HttpResponse(template.render(context, request))
def home(request):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    User = get_user_model()
    users = User.objects.all()
    object = Friends1.objects.filter(users1=request.user)
    return render(request, 'study_buddy_app/chat.html', {'user_firstname': request.user.first_name, 'user_lastname': request.user.last_name,'users': users, "friend_list": object})

# addclass API
def addclass_deptlist(request):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    response = requests.get('http://luthers-list.herokuapp.com/api/deptlist/?format=json').json()
    paginator = Paginator(response, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'study_buddy_app/addclassdeptlist.html', {'first': request.user.first_name,'last': request.user.last_name,'response':response, 'page_obj': page_obj})
# "
def dept(request, dept_name):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    classes = requests.get('http://luthers-list.herokuapp.com/api/dept/%s?format=json' %dept_name)
    response = classes.json()
    cur_classes = []
    for i in response:
        tmp = Class(subject=dept_name, catalog_number=i['catalog_number'], course_section=i['course_section'])
        tmp.save()
        cur_classes.append(tmp)
    return render(request, 'study_buddy_app/dept.html', {"first": request.user.first_name, "last": request.user.last_name, 'response':cur_classes, 'dept_name':dept_name})

# deleteclass API
def myclasses(request):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    profile = Profile.objects.get(user=request.user)
    classes = profile.classes.all()
    return render(request = request, template_name ="study_buddy_app/deleteclass.html", context = {"user":request.user, 'classes':classes})

# display only API
def deptlist(request):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    response = requests.get('http://luthers-list.herokuapp.com/api/deptlist/?format=json').json()
    paginator = Paginator(response, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'study_buddy_app/deptlist.html', {"first": request.user.first_name, "last": request.user.last_name, 'response': response, 'page_obj': page_obj})

# "
def dept_display_only(request, dept_name):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    classes = requests.get('http://luthers-list.herokuapp.com/api/dept/%s?format=json' %dept_name)
    response = classes.json()
    cur_classes = []
    for i in response:
        tmp = Class(subject=dept_name, catalog_number=i['catalog_number'], course_section=i['course_section'])
        tmp.save()
        cur_classes.append(tmp)
    paginator = Paginator(response, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'study_buddy_app/deptdisplay.html', {'response':cur_classes, 'dept_name':dept_name, 'page_obj': page_obj})

def room(request, room):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'study_buddy_app/room.html', {
        'first': request.user.first_name,
        'last': request.user.last_name,
        'username': username,
        'room': room,
        'room_details': room_details
    })

def go_to_chat(request):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    sender = request.user.username + " "
    sendee = request.POST['username'] + " "
    array = [sender, sendee]
    array.sort()
    room = ""


    array.sort()

    array[-1] = array[-1].strip(" ")

    for i in array:
        room = room + i

    object = Friends1.objects.filter(users1=request.user)

    friends = []

    for i in object:
        friends.append(str(i.current_user))
    print(friends)

    system_messages = messages.get_messages(request)
    for message in system_messages:
        # This iteration is necessary
        pass

    sendee = sendee.strip(" ")
    if str(sendee) not in friends:
        messages.success(request, "You are not friends with this person! Add them as a friend to chat with them again!")

    if Room.objects.filter(name=room).exists():
        return redirect('/study_buddy_app/home/'+room+'/?username='+sender)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/study_buddy_app/home/'+room+'/?username='+sender)

def checkview(request):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    room = ""
    sender = request.POST['username'] + " "
    sendee = request.POST.getlist('dropdown[]')
    array = [sender]

    for i in sendee:
        i = i + " "
        array.append(i)
    array.sort()

    array[-1] = array[-1].strip(" ")

    for i in array:
        room = room + i

    system_messages = messages.get_messages(request)
    for message in system_messages:
        # This iteration is necessary
        pass

    if room == array[0] and len(array) == 1:
        messages.success(request, "You must choose someone to talk to!")
        return redirect('/study_buddy_app/home/')

    elif Room.objects.filter(name=room).exists():
        return redirect('/study_buddy_app/home/'+room+'/?username='+sender)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/study_buddy_app/home/'+room+'/?username='+sender)

def send(request):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    message = request.POST['message']
    if not message:
        return
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.order_by('date').values())})


def user(request):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    try:
        user_form = UserForm(instance=request.user)
        profile = Profile.objects.get(user=request.user)
        classes = profile.classes.all()
        return render(request = request, template_name ="study_buddy_app/user.html", context = {"user":request.user, "user_form": user_form, 'classes':classes})
        # no_classes = classes.len() <= 0
        # return render(request = request, template_name ="study_buddy_app/user.html", context = {
        #     "user":request.user, 
        #     "user_form": user_form, 
        #     'classes':classes, 
        #     'no_classes': no_classes,
        # })
    except:
        User = get_user_model()
        users = User.objects.all()
        return render(request, 'study_buddy_app/chat.html', {'users': users})


def edituser(request):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    try:
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Changes Saved!")
        user_form = UserForm(instance=request.user)
        return render(request, 'study_buddy_app/edituser.html', context={'user':request.user, 'user_form':user_form})
    except: 
        User = get_user_model()
        users = User.objects.all()
        return render(request, 'study_buddy_app/chat.html', {'users': users})

def addclass(request):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    profile = Profile.objects.get(user=request.user)
    try:
        selected_class = Class.objects.get(pk=request.POST['class'])

        # only add class to profile if it's not already there
        already_exists = False
        for c in profile.classes.all():
            if selected_class.subject == c.subject and selected_class.catalog_number == c.catalog_number and selected_class.course_section == c.course_section:
                already_exists = True
        if not already_exists:
            profile.classes.add(selected_class)
            profile.save()

        return user(request)
    except(KeyError, Class.DoesNotExist):
        return render(request, 'study_buddy_app/dept.html', {
            'profile': profile,
            'error_message': "You didn't select a class.",
        })

def class_lookup(request, dept_name):
    try:
        selected_class = Class.objects.get(pk=request.POST['class'])

        subj = selected_class.subject
        cat_num = selected_class.catalog_number
        return redirect('/study_buddy_app/searchResults/?q=' + subj + "+" + cat_num + "/")
    except(KeyError, Class.DoesNotExist):
        return render(request, 'study_buddy_app/deptdisplay.html', {
            'error_message': "You didn't select a class.",
        })

# def courselist_actions(request):
#     try:
#         selected_class = Class.objects.get(pk=request.POST['class'])

#         if 'addclass' in request.POST:
#             if not request.user.is_authenticated:
#                 template = loader.get_template('socialaccount/login.html')
#                 context = {}
#                 return redirect('/study_buddy_app/accounts/google/login/')
#             profile = Profile.objects.get(user=request.user)

#             # only add class to profile if it's not already there
#             already_exists = False
#             for c in profile.classes.all():
#                 if selected_class.subject == c.subject and selected_class.catalog_number == c.catalog_number and selected_class.course_section == c.course_section:
#                     already_exists = True
#             if not already_exists:
#                 profile.classes.add(selected_class)
#                 profile.save()

#             return user(request)
#         else:
#             subj = selected_class.subject
#             cat_num = selected_class.catalog_number
#             return redirect('/study_buddy_app/searchResults/?q=' + subj + "+" + cat_num)
#     except(KeyError, Class.DoesNotExist):
#         return render(request, 'study_buddy_app/dept.html', {
#             'profile': profile,
#             'error_message': "You didn't select a class.",
#         })

def deleteclass(request):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    try:
        profile = Profile.objects.get(user=request.user)
        selected_class = Class.objects.get(pk=request.POST['class'])
        profile.classes.remove(selected_class)
        profile.save()
        return user(request)
    except(KeyError, Class.DoesNotExist):
        return render(request, 'study_buddy_app/deleteclass.html', {
            'profile': profile,
            'error_message': "You didn't select a class.",
        })
 
        
def publicProfile(request):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    try:
        user_form = UserForm(instance=request.user)
        return render(request = request, template_name ="study_buddy_app/publicProfile.html", context = {"user":request.user, "user_form": user_form})
    except:
        User = get_user_model()
        users = User.objects.all()
        return render(request, 'study_buddy_app/chat.html', {'users': users})
##class viewProfiles(generic.ListView):
##    template_name = 'study_buddy_app/viewProfiles.html'
##    context_object_name = 'profile_list'
##    def get_queryset(self):
##        return Profile.objects.all()
    
def send_friend_request(request,slug):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    #user = request.POST.get('username', False)
    sender = request.user
    x = sender.username
    recipient = User.objects.get(username = slug)
    model = FriendRequest.objects.get_or_create(sender=request.user,receiver=recipient)
    #return HttpResponse('friend request sent or already sent')
    system_messages = messages.get_messages(request)
    for message in system_messages:
        # This iteration is necessary
        pass
    messages.success(request, "Friend Request Sent or already Sent!")
    return redirect ('/study_buddy_app/publicProfile/'+slug)
    #return redirct('/study_buddy_app/search_resulsts/publicProfile/<slug:slug>/')

def delete_request(request, pk):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    client1 = User.objects.get(username=pk)
    #print(client1)
    #if operation == 'Sender_deleting':
    #    model1 = FriendRequest.objects.get(sender=request.user, recievers=client1)
     #   model1.delete()
    #elif operation == 'Reviever_deleting':
    model2 = FriendRequest.objects.get(sender=client1,receiver=request.user)
    model2.delete()
    #return HttpResponse('Request Deleted')
    return redirect('/study_buddy_app/user/friend_request/')


def remove_friend(request, pk):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    new_friend = User.objects.get(username=pk)
    Friends1.lose_friend(request.user, new_friend)
    Friends1.lose_friend(new_friend, request.user)
    #return HttpResponse('friend removed')
    return redirect('/study_buddy_app/user/friends/')


def accept_friend_request(request,pk):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    new_friend = User.objects.get(username = pk)
    fq = FriendRequest.objects.get(sender=new_friend, receiver=request.user)
    Friends1.make_friend(request.user, new_friend)
    Friends1.make_friend(new_friend, request.user)
    fq.delete()
    #return redirect('/studdy_buddy_app/user')
    #return HttpResponse('friend request accepted')
    return redirect('/study_buddy_app/user/friend_request/')


def viewRequest(request):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    try:
        object = FriendRequest.objects.filter(receiver = request.user)
        return render(request, 'study_buddy_app/friendRequest.html', {"first": request.user.first_name,"last": request.user.last_name,"request_list": object})
    except:
        User = get_user_model()
        users = User.objects.all()
        return render(request, 'study_buddy_app/chat.html', {'users': users})


def viewFriends(request):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    try:
        object = Friends1.objects.filter(users1 = request.user)
        return render(request, 'study_buddy_app/friends.html', {"first": request.user.first_name, "last": request.user.last_name, "friend_list": object})
    except:
        User = get_user_model()
        users = User.objects.all()
        return render(request, 'study_buddy_app/chat.html', {'users': users})
    
#new stuff
class viewProfiles(generic.ListView):
    template_name = 'study_buddy_app/viewProfiles.html'
    context_object_name = 'profile_list'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            template = loader.get_template('socialaccount/login.html')
            context = {}
            return redirect('/study_buddy_app/accounts/google/login/')
        return super(viewProfiles, self).get(request, *args, **kwargs)
    def get_queryset(self):
        return Profile.objects.all()

class listProfiles(generic.ListView):
    template_name = 'study_buddy_app/listProfiles.html'
    context_object_name = 'profile_list'
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            template = loader.get_template('socialaccount/login.html')
            context = {}
            return redirect('/study_buddy_app/accounts/google/login/')
        return super(listProfiles, self).get(request, *args, **kwargs)
    def get_queryset(self):
        return Profile.objects.all()
    
class DateForm(forms.Form):
    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date'}))
    start_time = forms.TimeField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'time'}))
    end_time = forms.TimeField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'time'}))

class seeProfile(generic.DetailView):

    model = Profile
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            template = loader.get_template('socialaccount/login.html')
            context = {}
            return redirect('/study_buddy_app/accounts/google/login/')
        return super(seeProfile, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(seeProfile, self).get_context_data(**kwargs)
        a = kwargs['object']
        b = a.user
        context['form'] = DateForm()
        context['friends'] = Friends1.objects.filter(users1 = self.request.user, current_user = b)
        context['first']=self.request.user.first_name
        context['last']= self.request.user.last_name
        return context

    
class ProfileMeeting(SingleObjectMixin, FormView):
    template_name = 'study_buddy_app/profile_detail.html'
    form_class = DateForm
    model = Profile
    def form_valid(self, form):
        self.process_user_input(form.cleaned_data)
        return super(ProfileMeeting, self).form_valid(form)
    
    def process_user_input(self, valid_data):
        # TODO: add to google calendar
        # TODO: add this meeting time to the model
        
        def generate_credentials():
            token = SocialToken.objects.get(account__user__username=self.request.user.username, app__provider="google")

            credentials = Credentials(
                token=token.token,
                refresh_token=token.token_secret,
                token_uri='https://oauth2.googleapis.com/token',
                client_id='562188647966-r0odsb07scpsnj3jr8hfcu7912jeke61.apps.googleusercontent.com', # replace with yours 
                client_secret='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') # replace with yours 
            service = build('calendar', 'v3', credentials=credentials)
        
            return service
        
        def create_google_calendar_event(date, start_time, end_time, profile_user):
            event = {
                'summary': 'Study buddy meeting',
                # TODO: generate zoom meeting
                'location': 'Zoom link: ',
                # TODO: put person's name in the profile and the class
                'description': 'You have a study meeting with '+str(profile_user.first_name) + " "+str(profile_user.last_name),
                'start': {
                    'dateTime': str(date)+"T"+str(start_time),
                    'timeZone': 'America/New_York',
                },
                'end': {
                    'dateTime': str(date)+"T"+str(end_time),
                    'timeZone': 'America/New_York',
                },
                'attendees': [
                    {'email': profile_user.email},
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            event = service.events().insert(calendarId='primary', body=event).execute()
        
        def add_event_to_calendar(date, start_time, end_time, profile_user):
            eastern = timezone('US/Eastern')
            start_datetime = datetime.combine(date, start_time, eastern)
            end_datetime = datetime.combine(date, end_time, eastern)
            start_str = start_datetime.strftime("%I:%M %p")
            end_str = end_datetime.strftime("%I:%M %p")

            event = Event(title="Meeting: "+profile_user.username,
                            description="Meeting with "+profile_user.first_name+" "+profile_user.last_name,
                            start_time=start_datetime,
                            end_time=end_datetime)
            event.save()
            

            self.request.user.event_set.add(event)
           
            copy = Event(title="Meeting: "+self.request.user.username,
                            description="Meeting with "+self.request.user.first_name+" "+self.request.user.last_name,
                            start_time=start_datetime,
                            end_time=end_datetime)
            copy.save()
            
            profile_user.event_set.add(copy)
        
        eastern = timezone('US/Eastern')
        start_datetime = datetime.combine(valid_data['date'], valid_data['start_time'], eastern)
        end_datetime = datetime.combine(valid_data['date'], valid_data['end_time'], eastern)
        system_messages = messages.get_messages(self.request)
        for message in system_messages:
            pass
        if start_datetime < end_datetime: 
            profile_user = User.objects.get(profile__slug=self.kwargs['slug'])
            
            googleSet = SocialAccount.objects.filter(provider="google")
            requestUser_isGoogle = len(googleSet.filter(user=self.request.user)) > 0
            
            profileUser_isGoogle = len(googleSet.filter(user=profile_user)) > 0
            
            if requestUser_isGoogle and profileUser_isGoogle:
                service = generate_credentials()
                create_google_calendar_event(valid_data['date'], valid_data['start_time'], valid_data['end_time'], profile_user)

            add_event_to_calendar(valid_data['date'], valid_data['start_time'], valid_data['end_time'], profile_user)
            system_messages = messages.get_messages(self.request)
            messages.success(self.request, "Successfully created event in calendar.")
        else:
            system_messages = messages.get_messages(self.request)
            messages.success(self.request, "Your meeting start time must be before end time.")
            return redirect('/study_buddy_app/')
        pass

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('profile-detail', kwargs={'slug': self.object.slug})

class ProfileDetail(View):
    template_name = 'study_buddy_app/profile_detail.html'
    def get(self, request, *args, **kwargs):
        view = seeProfile.as_view()
        return view(request,*args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ProfileMeeting.as_view()
        return view(request, *args, **kwargs)

class ProfileDetailSuccess(View):
    template_name = 'study_buddy_app/profile_detail.html'
    def get(self, request, *args, **kwargs):
        view = seeProfileSuccess.as_view()
        return view(request,*args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ProfileMeeting.as_view()
        return view(request, *args, **kwargs)

class seeProfileSuccess(generic.DetailView):

    model = Profile
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            template = loader.get_template('socialaccount/login.html')
            context = {}
            return redirect('/study_buddy_app/accounts/google/login/')
        return super(seeProfileSuccess, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(seeProfileSuccess, self).get_context_data(**kwargs)
        a = kwargs['object']
        b = a.user
        context['form'] = DateForm()
        context['friends'] = Friends1.objects.filter(users1 = self.request.user, current_user = b)
        context['first']=self.request.user.first_name
        context['last']= self.request.user.last_name
        context['successful_submit'] = True
        return context

def user_redirect(request):
    if not request.user.is_authenticated:
        template = loader.get_template('socialaccount/login.html')
        context = {}
        return redirect('/study_buddy_app/accounts/google/login/')
    user = request.POST['username']
    user_obj = User.objects.get(username=user)
    if user_obj.username == request.user.username:
        return redirect('/study_buddy_app/user/')
    return redirect('/study_buddy_app/publicProfile/'+user)

class CalendarView(generic.ListView):
    model = Event
    template_name = 'study_buddy_app/calendar.html'
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            template = loader.get_template('socialaccount/login.html')
            context = {}
            return redirect('/study_buddy_app/accounts/google/login/')
        return super(CalendarView, self).get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(self.request.user, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['user_firstname'] = self.request.user.first_name
        context['user_lastname'] = self.request.user.last_name
        # context['user_lastname'] = self.request.user.last_name
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
