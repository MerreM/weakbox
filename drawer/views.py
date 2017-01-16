from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from drawer.models import Token
from drawer.models import Value
import string
import random


@csrf_exempt
def register_application(request):
    '''
    Some old code that *sort-of* supplants the
    user with a token based model for uber simple auth.

    Probably a better way of doing this now...
    '''
    token = request.POST.get("token", False)
    if not token:
        new_token = generate_token()
        new_user = User.objects.create_user(username=new_token)
        Token.objects.create(user=new_user, token=new_token)
        return return_json(request, {"token": new_token})
    return HttpResponseBadRequest(
        "Token supplied - Application may already registered")


@csrf_exempt
def store_value(request, key, value=""):
    check_for_token(request)
    if Value.objects.filter(user=request.user, key=key).exists():
        Value.objects.filter(user=request.user, key=key).update(value=value)
    else:
        Value.objects.create(user=request.user, key=key, value=value)
    return return_json(request, {"success": True})


@csrf_exempt
def retrieve_value(request, key):
    check_for_token(request)
    if Value.objects.filter(user=request.user, key=key).exists():
        return return_json(
            request,
            Value.objects.get(user=request.user, key=key
                              ).to_dict())
    logout(request)
    return HttpResponseBadRequest("No key found.")


@csrf_exempt
def retrieve_all(request):
    check_for_token(request)
    output = [value.to_dict()
              for value in Value.objects.filter(user=request.user)]
    logout(request)
    return JsonResponse(output, safe=False)


def return_json(request, data):
    '''
    Util function left over from
    a lack oa JsonResponse object.
    Still logs users out though.
    '''
    logout(request)
    return JsonResponse(data)


def generate_token(length=64):
    return ''.join(
        random.choice(
            string.ascii_uppercase + string.digits
        ) for x in range(length))


def check_for_token(request):
    '''
    Simple auth util function.
    '''
    token = request.POST.get("token", False)
    if not token:
        raise PermissionDenied("No token supplied")
    user = authenticate(token=token)
    if user is not None:
        if user.is_active:
            login(request, user)
            return
    raise PermissionDenied("No token supplied")
