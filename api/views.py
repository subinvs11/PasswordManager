from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from user_management.models import CustomUser, Organization, PersonalPassword, OrganizationPassword
from api.serializers import SignUprSerializer, OrganizationSerializer, PersonalPasswordSerializer, \
OrganizationPasswordSerializer


class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignUprSerializer


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.is_active and user.is_staff:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key
            })
        else:
            return Response({
                'Error': "You don't have enough permission to perform this action!"
            })


class OrganizationView(APIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serialized_data = self.serializer_class(data=request.data)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response({'message': 'success'}, status=status.HTTP_200_OK)
            else:
                errors = serialized_data.errors
                return Response({'message': errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error = "Error in saving data %s " % e
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_object(self, pk):
        return Organization.objects.get(pk=pk)

    def put(self, request, pk):
        obj = self.get_object(pk)
        try:
            serialized_data = self.serializer_class(obj, data=request.data, partial=True)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response({'message': 'success'}, status=status.HTTP_200_OK)
            else:
                errors = serialized_data.errors
                return Response({'message': errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error = "Error in saving data %s " % e
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PersonalPasswordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PersonalPasswordSerializer
    queryset = PersonalPassword.objects.all()

    def get_serializer_context(self):
        return {'request': self.request, 'pk': self.kwargs.get('pk')}

    def create(self, request):
        try:
            serialized_data = self.serializer_class(data=request.data)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response({'message': 'success'}, status=status.HTTP_200_OK)
            else:
                errors = serialized_data.errors
                return Response({'message': errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error = "Error in saving data %s " % e
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        obj = self.get_object()
        try:
            serialized_data = self.serializer_class(obj, data=request.data, partial=True)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response({'message': 'success'}, status=status.HTTP_200_OK)
            else:
                errors = serialized_data.errors
                return Response({'message': errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error = "Error in saving data %s " % e
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrganizationPasswordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationPasswordSerializer
    queryset = OrganizationPassword.objects.all()

    def get_serializer_context(self):
        return {'request': self.request, 'pk': self.kwargs.get('pk')}

    def create(self, request):
        try:
            serialized_data = self.serializer_class(data=request.data)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response({'message': 'success'}, status=status.HTTP_200_OK)
            else:
                errors = serialized_data.errors
                return Response({'message': errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error = "Error in saving data %s " % e
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        obj = self.get_object()
        try:
            serialized_data = self.serializer_class(obj, data=request.data, partial=True)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response({'message': 'success'}, status=status.HTTP_200_OK)
            else:
                errors = serialized_data.errors
                return Response({'message': errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error = "Error in saving data %s" % e
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
