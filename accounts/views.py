import string

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, UserloginotpModel, UserProfileModel, UserCartModel, UserCartProductModel
from .serializers import AllUserSerializer, CartSerializer, CartPSerializer
from rest_framework import status
from django.core.mail import send_mail
from TestOne.settings import EMAIL_HOST_USER
import random
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from django.contrib.auth.backends import ModelBackend


class PasswordlessAuthBackend(ModelBackend):
    def authenticate(self, email=None, **kwargs):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class CreateView(APIView):
    def get(self, request):
        query = User.objects.all()
        serializer = AllUserSerializer(query, many=True)
        context = {
            "status": status.HTTP_200_OK,
            "error": None,
            "data": serializer.data
        }
        return Response(data=context, status=status.HTTP_200_OK)

    def post(self, request):
        # Phone_number,Email,
        # Name,Date_of_birth,Gender,Image
        email = request.POST["email"]
        phone = request.POST["phone"]
        name = request.POST["name"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        image = request.data["image"]
        if not User.objects.filter(email=email).exists():
            user = User.objects.create(email=email, phone=phone, is_customer=True)
            user.save()
            userprofile = UserProfileModel.objects.create(owner=user, name=name, dob=dob, gender=gender, image=image)
            userprofile.save()
        return Response(data={"Status": "User Created."})


class LoginView(APIView):
    def get(self, request, email):
        if User.objects.filter(email=email).exists():
            otp = ''.join(random.choice(string.digits) for i in range(4))
            subject = 'OTP'
            msg = f'OTP is {otp}'
            send_to = email
            send_mail(subject, msg, EMAIL_HOST_USER,
                      [send_to], fail_silently=False)
            context = {
                "status": status.HTTP_200_OK,
                "error": None,
                "data": "OTP Send."
            }
            user = User.objects.get(email=email)
            if UserloginotpModel.objects.filter(owner=user).exists():
                UserloginotpModel.objects.update(otp=otp).save()
            else:
                UserloginotpModel.objects.create(owner=user, otp=otp).save()
            return Response(data=context, status=status.HTTP_200_OK)
        else:
            context = {
                "status": status.HTTP_404_NOT_FOUND,
                "error": True,
                "data": "Email Not Found."
            }
            return Response(data=context, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, email):
        otp = int(request.POST["otp"])
        user = User.objects.get(email=email)
        try:
            userotp = UserloginotpModel.objects.get(owner=user)
            if userotp.otp == otp:
                user = PasswordlessAuthBackend.authenticate(self, email=email)
                is_Login = RefreshToken.for_user(user)
                context = {
                    "status": status.HTTP_200_OK,
                    "error": None,
                    "data": {
                        "token": {
                            "refresh_token": str(is_Login),
                            "access_token": str(is_Login.access_token),
                        },
                    },
                }
                userotp.active = True
                return Response(context, status=status.HTTP_200_OK)
        except UserloginotpModel.DoesNotExist:
            return Response("OOPS")


class CartView(APIView):
    def get(self, request):
        query = UserCartModel.objects.all()
        serializer = CartSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("Error", status=status.HTTP_200_OK)
