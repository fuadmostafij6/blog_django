from rest_framework import status, generics
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterUserSerializer, LoginUserSerializer, UpdateUserSerializer

User = get_user_model()


class RegisterUserView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            email_id = serializer.validated_data['email_id']
            name = serializer.validated_data['name']
            phone_number = serializer.validated_data['phone_number']

            password = request.data.get('password')

            user = User.objects.create(
                username=username,
                email_id=email_id,
                name=name,
            )

            user.set_password(password)
            user.save()

            token, created = Token.objects.get_or_create(user=user)

            content = {
                'token': token.key,
                'user_uid': user.user_uid,
                'username': username,
                'email_id': email_id,
                'name': name,
                'about_me': user.about_me,
                'phone_number': phone_number,
                'profile_picture': user.profile_picture.url if user.profile_picture else None,
            }

            response_content = {
                'status': True,
                'message': 'User registered successfully.',
                'data': content
            }

            return Response(response_content, status=status.HTTP_201_CREATED)

        else:
            response_content = {
                'status': False,
                'message': serializer.errors,
            }

            print(response_content)
            return Response(response_content, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            if serializer.is_valid():
                username = serializer.validated_data['username']

                user = User.objects.get(username=username)

                token, created = Token.objects.get_or_create(user=user)

                content = {

                    'token': token.key,
                    'user_uid': user.user_uid,
                    'username': username,
                    'email_id': user.email_id,
                    'name': user.name,
                    'about_me': user.about_me,
                    'profile_picture': user.profile_picture.url if user.profile_picture != '' else None
                }

                response_content = {
                    'status': True,
                    'message': 'User logged in successfully.',
                    'data': content
                }

                return Response(response_content, status=status.HTTP_200_OK)

            else:
                response_content = {
                    'status': False,
                    'message': serializer.errors,
                }

                return Response(response_content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)


class LogoutUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        token = Token.objects.get(user=user)

        token.delete()

        response_content = {
            'status': True,
            'message': 'User logged out successfully.'

        }

        return Response(response_content, status=status.HTTP_202_ACCEPTED)


class UpdateProfileView(APIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

    def put(self, request, pk, format=None):
        user = User.objects.get(user_uid=pk)
        serializer = UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_content = {
                'status': True,
                'message': 'User update successfully.',
                'data': serializer.data
            }
            return Response(response_content)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
