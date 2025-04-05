from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from .models import RemoteSession
import uuid
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
#using a function authenticate from django.contrib.auth
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        return Response({'error': 'Invalid credentials'}, status=400)
    

class StartSessionView(APIView):
    #only logged in users can start a session
    permission_classes = [IsAuthenticated]

    def post(self, request):
        session_id = str(uuid.uuid4())[:8]  # Generate a short session ID
        session = RemoteSession.objects.create(user=request.user, session_id=session_id)
        return Response({"session_id": session.session_id, "message": "Session started"})