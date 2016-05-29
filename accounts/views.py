import sys
from django.contrib.auth import authenticate, login
from django.contrib.auth import ( login as auth_login,
                                  logout as auth_logout
                                )
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.http.response import HttpResponse


# Create your views here.

# def login(request):
#     print('login view', file = sys.stderr)
#     user = authenticate(assertion=request.POST['assertion'])
#     if user is not None:
#         auth_login(request, user)
#     return redirect('/')
# 
# def logout(request):
#     auth_logout(request)
#     return redirect('/')

def persona_login(request):
    user = authenticate(assertion = request.POST['assertion'])
    if user:
        login(request, user)
    return HttpResponse('OK')


    
