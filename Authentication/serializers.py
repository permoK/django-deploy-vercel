# serializers.py
from rest_framework import serializers
from .models import Farmer, Cow

class FarmerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Farmer
        fields = ['id', 'full_name', 'county', 'telephone', 'farm_name', 'email', 'password']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        farmer = Farmer(**validated_data)
        farmer.username = validated_data['email']  # Using email as username
        farmer.set_password(password)
        farmer.save()
        return farmer

class CowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cow
        fields = ['id', 'name', 'weight', 'breed_type', 'gender', 'age', 'created_at']
        read_only_fields = ['farmer']


# Farmer serializer for all farmers
class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = '__all__'

