from django.contrib.auth import logout
from django.db import transaction
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
import logging

from config import settings
from users.models import CustomUser
from users.serializers import CustomUserSerializer, CustomTokenObtainPairSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"], url_path="toggle-admin")
    def toggle_admin(self, request, pk=None):
        """Foydalanuvchining admin huquqini yoqish yoki o'chirish"""
        if not request.user.is_staff:
            return Response(
                {"error": "Sizda bu amalni bajarish uchun huquq yo'q!"},
                status=status.HTTP_403_FORBIDDEN
            )

        user = self.get_object()

        # 2. Admin o'zini o'zi tasodifan adminlikdan mahrum qilib qo'ymasligi uchun himoya (ixtiyoriy)
        if user == request.user:
            return Response(
                {"error": "O'zingizning admin huquqingizni o'zgartira olmaysiz!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_staff = not user.is_staff
        user.save()

        return Response({
            "status": "success",
            "message": f"{user.phone_number} uchun admin huquqi {'berildi' if user.is_staff else 'olib tashlandi'}.",
            "is_staff": user.is_staff
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="toggle-active")
    def toggle_active(self, request, pk=None):
        """Foydalanuvchini bloklash yoki blokdan chiqarish"""
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        return Response({
            "status": "success",
            "message": f"'{user.phone_number}' faolligi: {user.is_active}"
        })


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


logger = logging.getLogger(__name__)


class LogoutJWTView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Front-end'dan JSON orqali "refresh" token keladi: {"refresh": "your_token..."}
        refresh_token = request.data.get("refresh")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError as e:
                logger.warning("Refresh token blacklist failed: %s", str(e))
                return Response({"detail": "Token yaroqsiz yoki allaqachon bekor qilingan."},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Refresh token taqdim etilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Tizimdan muvaffaqiyatli chiqildi."}, status=status.HTTP_200_OK)






