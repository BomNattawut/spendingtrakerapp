from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import RegisterSerializer, BudgetSerializer, ExpenseCategorySerializer, ExpensesSerializer, UserProfileSerializer
from django.contrib.auth import authenticate, login, logout
from .models import Budget, ExpenseCategory, Expense,Profile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework import permissions
import logging
import os

logger = logging.getLogger(__name__)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        profile = user.profile  # ดึง Profile ที่เกี่ยวข้องกับผู้ใช้
        serializer = UserProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            if 'profile_picture' in request.FILES:
                # ลบไฟล์เก่าถ้ามี
                if profile.profile_picture:
                    if os.path.isfile(profile.profile_picture.path):  # ตรวจสอบว่ามีไฟล์อยู่ในโฟลเดอร์หรือไม่
                        os.remove(profile.profile_picture.path)  # ลบไฟล์เก่า

                profile.profile_picture = request.FILES['profile_picture']  # อัปเดตรูปภาพใหม่
                profile.save()  # บันทึก Profile

            serializer.save()  # บันทึกข้อมูลผู้ใช้
            return Response({"message": "Profile updated successfully", "profile_picture": profile.profile_picture.url}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # บันทึกผู้ใช้ใหม่
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)  # สร้างหรือดึง token
            # เพิ่ม user_id ใน response
            return Response({
                "message": "Login successful",
                "token": token.key,
                "user_id": user.id  # ส่ง user_id กลับมา
            }, status=status.HTTP_200_OK)
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()  # ลบ token ของผู้ใช้
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

class BudgetCreateView(APIView):
    permission_classes = [IsAuthenticated]  # เพิ่ม permission นี้

    def post(self, request):
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # เชื่อมโยงกับผู้ใช้ที่ล็อกอินอยู่
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BudgetListView(APIView):
    permission_classes = [IsAuthenticated]  # เพิ่ม permission นี้

    def get(self, request):
        user = request.user  # ดึงข้อมูลผู้ใช้ที่ล็อกอินอยู่
        budgets = Budget.objects.filter(user=user)  # ดึงงบประมาณของผู้ใช้
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data)

class ExpenseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        expenses = Expense.objects.filter(user=user)
        serializer = ExpensesSerializer(expenses, many=True)
        return Response(serializer.data)

class ExpenseCategoryListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        categories = ExpenseCategory.objects.all()  # ดึงข้อมูลทุกประเภทการใช้จ่าย
        serializer = ExpenseCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExpenseFormView(APIView):
    permission_classes = [IsAuthenticated]  # กำหนดให้ต้องล็อกอินก่อนจึงจะใช้งานได้

    def post(self, request):
        logger.info(f"Request data: {request.data}")
        serializer = ExpensesSerializer(data=request.data, context={'request': request})  # ส่ง context
        if serializer.is_valid():
            serializer.save(user=request.user)  # เชื่อมโยงกับผู้ใช้ที่ล็อกอินอยู่
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BudgetDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, budgetId):
        try:
            budget = Budget.objects.get(pk=budgetId, user=request.user)
            budget.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Budget.DoesNotExist:
            return Response({"error": "Budget not found or you do not have permission to delete it."},
                            status=status.HTTP_404_NOT_FOUND)

class ExpenseDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request,expenseId ):
        try:
            expense = Expense.objects.get(pk=expenseId, user=request.user)  # ตรวจสอบว่าผู้ใช้เป็นเจ้าของ
            expense.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Expense.DoesNotExist:
            return Response({"error": "Expense not found or you do not have permission to delete it."},
                            status=status.HTTP_404_NOT_FOUND)
