from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from rest_framework import viewsets
from social.serializers import MessageSerializer, MemberSerializer

from social.models import Member, Profile, Message

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.order_by('id')
    serializer_class = MessageSerializer    
    
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.order_by('username')
    serializer_class = MemberSerializer    


appname = 'Facemagazine'

def index(request):
    template = loader.get_template('social/index.html')
    context = RequestContext(request, {
            'appname': appname,
        })
    return HttpResponse(template.render(context))

def messages(request, view_user):
    if 'username' in request.session:
        username = request.session['username']
        userMember = Member.objects.get(pk=username)
        viewMember = Member.objects.get(pk=view_user)
        viewname = viewMember.username
        
        #Looking at own inbox
        if view_user == username:
            greeting = "Your"
            canDelete = True;
            public_messages = Message.objects.filter(receiver=username).filter(is_private=False)
            private_messages = Message.objects.filter(receiver=username).filter(is_private=True)
        #Looking at public messages sent to other user along with private messages you sent the other user
        else:
            canDelete = False;
            greeting = view_user + "'s"
            public_messages = Message.objects.filter(receiver=viewname).filter(is_private=False)
            private_messages = Message.objects.filter(sender=username).filter(receiver=viewname).filter(is_private=True)
        
        #Delete messages in your inbox  
        if 'remove' in request.GET:
            messageid = request.GET['remove']
            Message.objects.filter(id=messageid).delete()
        
        #Reply to messages -> redirects you to the sender's page
        if 'reply' in request.GET:
            senderName = request.GET['reply']
            return HttpResponseRedirect(senderName)

        #Posting a new message
        if 'text' in request.POST:
            text = request.POST['text']
            #takes value from checkbox
            if 'is_private' in request.POST:
                private = True
            else:
                private = False
        
            #creates message object (as defined in models) and commits it to the database
            message = Message(  message=text, 
                                is_private=private, 
                                sender=userMember,  
                                receiver=viewMember)
            message.save()
            text = ""
        else:
            text = ""

        template = loader.get_template('social/messages.html')
        context = RequestContext(request, {
                'appname': appname,
                'username': username,
                'greeting': greeting,
                'viewName' : viewname,
                'loggedin': True,
                'public_messages': public_messages,
                'private_messages': private_messages,
                'canDelete' : canDelete,
                'text': text,
            })

        return HttpResponse(template.render(context))
    else:
        template = loader.get_template('social/login.html')
        error = "User is not logged it, no access to messages page!"
        context = RequestContext(request, {
            'appname': appname, 
            'error' : error,
        })
        return HttpResponse(template.render(context))



def signup(request):
    template = loader.get_template('social/signup.html')
    context = RequestContext(request, {
            'appname': appname,
        })
    return HttpResponse(template.render(context))

def register(request):
    u = request.POST['user']
    p = request.POST['pass']
    user = Member(username=u, password=p)
    user.save()
    template = loader.get_template('social/user-registered.html')    
    context = RequestContext(request, {
        'appname': appname,
        'username' : u
        })
    return HttpResponse(template.render(context))

def login(request):
    if 'username' not in request.POST:
        template = loader.get_template('social/login.html')
        context = RequestContext(request, {
                'appname': appname, 
            })
        return HttpResponse(template.render(context))
    else:
        u = request.POST['username']
        p = request.POST['password']
        try:
            member = Member.objects.get(pk=u)
        except Member.DoesNotExist:
            template = loader.get_template('social/login.html')
            error = "User " + u + " does not exist"
            context = RequestContext(request, {
                'appname': appname, 
                'error' : error,
            })
            return HttpResponse(template.render(context))
        if member.password == p:
            request.session['username'] = u;
            request.session['password'] = p;
            return render(request, 'social/login.html', {
                'appname': appname,
                'username': u,
                'loggedin': True}
                )
        else:
            template = loader.get_template('social/login.html')
            error = "Incorrect Password!"
            context = RequestContext(request, {
                'appname': appname, 
                'error' : error,
            })
            return HttpResponse(template.render(context))

def logout(request):
    if 'username' in request.session:
        u = request.session['username']
        request.session.flush()        
        template = loader.get_template('social/logout.html')
        context = RequestContext(request, {
                'appname': appname,
                'username': u
            })
        return HttpResponse(template.render(context))
    else:
        template = loader.get_template('social/login.html')
        error = "Cannot logout you are not logged in"
        context = RequestContext(request, {
            'appname': appname, 
            'error' : error,
        })
        return HttpResponse(template.render(context))

def member(request, view_user):
    if 'username' in request.session:
        username = request.session['username']
        member = Member.objects.get(pk=view_user)

        if view_user == username:
            greeting = "Your"
        else:
            greeting = view_user + "'s"

        if member.profile:
            text = member.profile.text
        else:
            text = ""
        return render(request, 'social/member.html', {
            'appname': appname,
            'username': username,
            'member' : member,
            'greeting': greeting,
            'profile': text,
            'loggedin': True}
            )
    else:
        template = loader.get_template('social/login.html')
        error = "User is not logged it, no access to members page!"
        context = RequestContext(request, {
            'appname': appname, 
            'error' : error,
        })
        return HttpResponse(template.render(context))

def friends(request):
    if 'username' in request.session:
        username = request.session['username']
        member_obj = Member.objects.get(pk=username)
        # list of people I'm following
        following = member_obj.following.all()
        # list of people that are following me
        followers = Member.objects.filter(following__username=username)
        # render reponse
        return render(request, 'social/friends.html', {
            'appname': appname,
            'username': username,
            'members': members,
            'following': following,
            'followers': followers,
            'loggedin': True}
            )
    else:
        template = loader.get_template('social/login.html')
        error = "User is not logged it, no access to friends page!"
        context = RequestContext(request, {
            'appname': appname, 
            'error' : error,
        })
        return HttpResponse(template.render(context))

def members(request):
    if 'username' in request.session:
        username = request.session['username']
        member_obj = Member.objects.get(pk=username)
        # follow new friend
        if 'add' in request.GET:
            friend = request.GET['add']
            friend_obj = Member.objects.get(pk=friend)
            member_obj.following.add(friend_obj)
            member_obj.save()
        # unfollow a friend
        if 'remove' in request.GET:
            friend = request.GET['remove']
            friend_obj = Member.objects.get(pk=friend)
            member_obj.following.remove(friend_obj)
            member_obj.save()
        # view user profile
        if 'view' in request.GET:
            return member(request, request.GET['view'])
        else:
            # list of all other members
            members = Member.objects.exclude(pk=username)
            # list of people I'm following
            following = member_obj.following.all()
            # list of people that are following me
            followers = Member.objects.filter(following__username=username)
            # render reponse
            return render(request, 'social/members.html', {
                'appname': appname,
                'username': username,
                'members': members,
                'following': following,
                'followers': followers,
                'loggedin': True}
                )
    else:
        template = loader.get_template('social/login.html')
        error = "User is not logged it, no access to members page!"
        context = RequestContext(request, {
            'appname': appname, 
            'error' : error,
        })
        return HttpResponse(template.render(context))

def profile(request):
    if 'username' in request.session:
        u = request.session['username']
        member = Member.objects.get(pk=u)
        if 'text' in request.POST:
            text = request.POST['text']
            if member.profile:
                member.profile.text = text
                member.profile.save()
            else:
                profile = Profile(text=text)
                profile.save()
                member.profile = profile
            member.save()
        else:
            if member.profile:
                text = member.profile.text
            else:
                text = ""
        return render(request, 'social/profile.html', {
            'appname': appname,
            'username': u,
            'text' : text,
            'loggedin': True}
            )
    else:
        template = loader.get_template('social/login.html')
        error = "User is not logged it, no access to profiles page!"
        context = RequestContext(request, {
            'appname': appname, 
            'error' : error,
        })
        return HttpResponse(template.render(context))

def checkuser(request):
    if 'user' in request.POST:
        u = request.POST['user']
        try:
            member = Member.objects.get(pk=u)
        except Member.DoesNotExist:
            member = None
        if member is not None:
            return HttpResponse("<span class='taken'>&nbsp;&#x2718; This username is taken</span>")
        else:
            return HttpResponse("<span class='available'>&nbsp;&#x2714; This username is available</span>")           
            
            
