from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from drawer.models import Token
from drawer.models import Value
import json
import string
import random

@csrf_exempt
def registerApplication(request):
    token = request.POST.get("token",False)
    if not token:
        new_token = generateToken()
        new_user = User.objects.create_user(username=new_token)
        Token.objects.create(user=new_user,token=new_token)
        return returnJsonResponse(request,{"token":new_token})
    print token
    return HttpResponseBadRequest("Token supplied - Application may already registered")

@csrf_exempt
def storeValue(request,key,value=""):
    checkForToken(request)
    if Value.objects.filter(user=request.user,key=key).exists():
        Value.objects.filter(user=request.user,key=key).update(value=value)
    else:
        Value.objects.create(user=request.user,key=key,value=value)
    return returnJsonResponse(request,{"success":True})


@csrf_exempt
def retrieveValue(request,key):
    checkForToken(request)
    if Value.objects.filter(user=request.user,key=key).exists():
        return returnJsonResponse(request,Value.objects.get(user=request.user,key=key).to_dict())    
    return returnJsonResponse(request,{})

@csrf_exempt
def retrieveAll(request):
    checkForToken(request)
    output = [value.to_dict() for value in Value.objects.filter(user=request.user)]
    return returnJsonResponse(request,output)

def returnJsonResponse(request,data):
    logout(request)
    return HttpResponse(json.dumps(data),content_type="application/json")

def generateToken(length=64):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(length))

def checkForToken(request):
    token = request.POST.get("token",False)
    if not token:
        raise PermissionDenied("No token supplied")
    user = authenticate(token=token)
    if user is not None:
        if user.is_active:
            login(request,user)
            return
    raise PermissionDenied("No token supplied")
