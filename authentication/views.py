from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from authentication.tokens import account_activation_token
# Create your views here.

class UsernameValidationView(View):
  def post(self,request):
    data = json.loads(request.body)
    username = data['username']
    
    if not str(username).isalnum():
      return JsonResponse({"username_error":"username should only contain alphanumeric character"},status=400)
    if User.objects.filter(username=username).exists():
      return JsonResponse({"username_error":"sorry the username in use, choose another one"},status=409)
    return JsonResponse({"username_valid":True})


class EmailValidationView(View):
  def post(self,request):
    data = json.loads(request.body)
    email = data['email']

    if not validate_email(email):
      return JsonResponse({"email_error":"Email is invalid"},status=400)
    if User.objects.filter(email=email).exists():
      return JsonResponse({"email_error":"sorry the email in use, choose another one"},status=409)
    return JsonResponse({"email_valid":True})

class RegistrationView(View):
  def get(self,request):
    return render(request, 'authentication/register.html')
  def post(self,request):
    username = request.POST["username"]
    email = request.POST['email']
    password = request.POST['password']

    context = {
      "fieldvalues":request.POST
    }

    if not User.objects.filter(username=username).exists():
      if not User.objects.filter(email=email).exists():
        if len(password) < 6:
          messages.error(request,"Password too short")
          return render(request, 'authentication/register.html',context)
        user = User.objects.create_user(username=username,email=email)
        user.set_password(password)
        user.is_active=False
        user.save()
      
         # encode uid
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        # getting domain we are on
        domain=get_current_site(request).domain
        # relative url to verifiction
        link = reverse('activate',kwargs={
          'uidb64':uidb64,'token':account_activation_token.make_token(user)
        })
        activate_url = 'http://'+domain+link
        email_body = 'Hi '+user.username+' Please user this link to verify you account\n'+activate_url
        email_subject = 'Activate your account'
        
        email = EmailMessage(
          email_subject,
          email_body,
          'noreply@semycolon.com',
          [email]
        )
        email.send(fail_silently=False)

        messages.success(request,"Account Succesfully Created")
        return render(request, 'authentication/register.html')
        
    return render(request, 'authentication/register.html')
  
class VerificationView(View):
  def get(self,request,uidb64,token):

    try:
      id = force_str(urlsafe_base64_decode(uidb64))
      user = User.objects.get(pk=id)

      if not account_activation_token.check_token(user,token):
        return redirect("login"+"?messages"+"User already activated")
      if user.is_active:
        return redirect("login")
      user.is_active=True
      user.save()

      messages.success(request,"Account activated successfully")
      return redirect('login') 
    except Exception as ex:
      pass
    return redirect('login') 
  
class LoginView(View):
  def get(self,request):
    return render(request,"authentication/login.html")
  def post(self,request):
    username = request.POST['username']
    password = request.POST['password']

    if username and password:
      user = auth.authenticate(username=username,password=password)
      if user:
        if user.is_active:
          auth.login(request,user)
          messages.success(request,"welcome," + user.username+ " you are now loged in")
          return redirect("expenses")
        else:
          messages.error(request,"account is not active,please check you email")
          return render(request,"authentication/login.html")
      else:
        messages.error(request,"Invalid Credentials,tyr again")
        return render(request,"authentication/login.html")
    else:
      messages.error(request,"Please fill all fields")
      return render(request,"authentication/login.html")
  
    
class LogoutView(View):
  def post(self,request):
    auth.logout(request)
    messages.success(request,"you have been logged out")
    return redirect("login")