from profile import Profile

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Profile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Неверные учетные данные.")
        return user



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name','last_name']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['hotel_image']


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['room_image']


class RoomListSerializer(serializers.ModelSerializer):
    room_images = RoomImageSerializer(many =True, read_only=True)

    class Meta:
        model = Room
        fields = ['id','room_images', 'room_number', 'room_type', 'room_status', 'room_price']


class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'room_status', 'room_price', 'all_inclusive', 'room_description']


class ReviewSerializer(serializers.ModelSerializer):
    user_name = UserProfileSimpleSerializer

    class Meta:
        model = Review
        fields = ['user_name', 'text', 'stars', 'parent']


class HotelListSerializer(serializers.ModelSerializer):
    hotel_images = HotelImageSerializer(many= True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['id','hotel_name', 'hotel_images', 'address', 'hotel_stars','avg_rating','get_count_people']


    def get_avg_rating(self, obj):
     return obj.get_avg_rating()

    def get_count_people(self,obj):
        return obj.get_count_people()


class CountryDetailSerializer(serializers.ModelSerializer):
    hotels = HotelListSerializer(many= True, read_only=True)

    class Meta:
        model = Country
        fields = ['country_name', 'hotels']


class HotelDetailSerializer(serializers.ModelSerializer):
    hotel_images = HotelImageSerializer(many= True, read_only=True)
    country = CountrySerializer()
    owner = UserProfileSimpleSerializer
    created_date = serializers.DateField(format('%d-%m-%Y'))
    rooms = RoomListSerializer(many=True, read_only = True)
    reviews = ReviewSerializer(many=True, read_only = True)

    class Meta:
        model = Hotel
        fields = ['hotel_name', 'hotel_description','city','country',
                  'address','hotel_video','created_date', 'hotel_stars', 'hotel_images','owner','rooms','reviews']


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


