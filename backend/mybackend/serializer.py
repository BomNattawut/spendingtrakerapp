from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Expense, Budget, ExpenseCategory, Profile
import os
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_picture']

    def update(self, instance, validated_data):
        # ตรวจสอบว่ามีการอัปโหลด profile_picture ใหม่หรือไม่
        if 'profile_picture' in validated_data:
            # ถ้ามี ให้ลบไฟล์เก่าออก
            if instance.profile_picture:
                old_file_path = instance.profile_picture.path  # ได้พาธของไฟล์เก่า
                if os.path.isfile(old_file_path):
                    os.remove(old_file_path)  # ลบไฟล์เก่า

            # ตั้งค่าภาพโปรไฟล์ใหม่
            instance.profile_picture = validated_data['profile_picture']
        
        instance.save()  # บันทึกการเปลี่ยนแปลง
        return instance  # ส่งคืนโปรไฟล์ที่ได้รับการอัปเดต

class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source='profile.profile_picture', required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'profile_picture']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()

        # อัปเดตโปรไฟล์
        profile_data = validated_data.get('profile', {})
        profile = instance.profile if hasattr(instance, 'profile') else Profile.objects.create(user=instance)
        profile.profile_picture = profile_data.get('profile_picture', profile.profile_picture)
        profile.save()

        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])  # Hash password
        user.save()
        Profile.objects.create(user=user)  # Create profile for new user
        return user

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['budgetid','amount', 'category', 'description', 'start_date', 'end_date']
        read_only_fields = ['user']

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name', 'description']

class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['user','expenseid', 'description', 'amount', 'date', 'category']
        extra_kwargs = {
            'user': {'read_only': True}  # Make user field read-only
        }

    def post(self, request, *args, **kwargs):
        serializer = ExpensesSerializer(data=request.data)
        if serializer.is_valid():
        # ไม่ต้องส่ง user เข้าไปที่นี่ เพราะมันจะถูกดึงจาก context
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

