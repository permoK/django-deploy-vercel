# views.py
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import FarmerRegistrationSerializer, CowSerializer, FarmerSerializer
from .models import Cow, Farmer

class FarmerRegistrationView(APIView):
    def post(self, request):
        serializer = FarmerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            farmer = serializer.save()
            refresh = RefreshToken.for_user(farmer)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                'user_id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'phone_number': user.telephone,
                'subscription_status': user.subscription_status,
                'streak': user.streak,
                }
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class FarmerDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        farmer = request.user  # Get the currently logged-in user
        user_data = {
            'id': farmer.id,
            'county': farmer.county,
            'email': farmer.email,
            'farm_name': farmer.farm_name,
            'telephone': farmer.telephone,
            # Include any additional fields as needed
        }
        return Response(user_data, status=status.HTTP_200_OK)
    
    # get all the farmers in the system
    def get(self, request):

        allFarmers = Farmer.objects.all() 
        serializer = FarmerSerializer(allFarmers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(farmer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, cow_id=None):
        # Retrieve all cows, or filter by cow_id and/or farmer_id
        farmer_id = request.query_params.get('farmer_id')
        
        # Filter based on provided parameters
        cows = Cow.objects.all()

        # Filter cows by farmer ID if provided
        if farmer_id:
            try:
                farmer = Farmer.objects.get(id=farmer_id)
                cows = cows.filter(farmer=farmer)
            except Farmer.DoesNotExist:
                return Response(
                    {"error": "Farmer not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        # If cow_id is provided, filter further by cow ID
        if cow_id:
            cows = cows.filter(id=cow_id)

        # Filter cows belonging to the requesting user
        cows = cows.filter(farmer=request.user)

        # Serialize and return data
        if cow_id:
            if cows.exists():
                serializer = CowSerializer(cows.first())
                return Response(serializer.data)
            else:
                return Response(
                    {"error": "Cow not found or you do not have permission to access this cow."},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            serializer = CowSerializer(cows, many=True)
            return Response(serializer.data)

# methane endpoint


# server warming
def index(request):
    return HttpResponse("index")

import requests
from django.http import HttpResponse, JsonResponse

def ping_serverless(request):
    try:
        response = requests.get('https://kapshackathonbackend.onrender.com/')
        response.raise_for_status()
        return JsonResponse({'status': 'success', 'message': 'Server pinged successfully'})
    except requests.RequestException as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

