from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SectionSerializer

from django.contrib.auth.hashers import make_password, check_password

from .models import *
from .serializers import *

# ✅ JWT
import jwt
from datetime import datetime, timedelta


# =========================
# READ-ONLY APIs
# =========================

class NavbarViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Navbar.objects.all()
    serializer_class = NavbarSerializer


class MenuItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class DropdownItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DropdownItem.objects.all()
    serializer_class = DropdownItemSerializer


class HeroViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer


class InfrastructureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InfrastructureCard.objects.all()
    serializer_class = InfrastructureSerializer


class VisibilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Visibility.objects.all()
    serializer_class = VisibilitySerializer


class VisibilityCardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VisibilityCard.objects.all()
    serializer_class = VisibilityCardSerializer


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class FooterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Footer.objects.all()
    serializer_class = FooterSerializer


class FooterSectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FooterSection.objects.all()
    serializer_class = FooterSectionSerializer


class FooterItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FooterItem.objects.all()
    serializer_class = FooterItemSerializer


# =========================
# FULL CRUD APIs
# =========================

class DemoViewSet(viewsets.ModelViewSet):
    queryset = Demo.objects.all()
    serializer_class = DemoSerializer


class DemoFormViewSet(viewsets.ModelViewSet):
    queryset = DemoForm.objects.all()
    serializer_class = DemoFormSerializer


class DemoFormSubmissionViewSet(viewsets.ModelViewSet):
    queryset = DemoFormSubmission.objects.all()
    serializer_class = DemoFormSubmissionSerializer


class PortfolioDataViewSet(viewsets.ModelViewSet):
    queryset = PortfolioData.objects.all()
    serializer_class = PortfolioDataSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


# =========================
# 🔐 LOGIN API (JWT)
# =========================

@api_view(['POST'])
def login_view(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {"message": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email=email).first()

        if not user:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not check_password(password, user.password):
            return Response(
                {"message": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        payload = {
            "user_id": user.id,
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }

        token = jwt.encode(payload, "secret123", algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode("utf-8")

        return Response({
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user.id,
                "email": user.email
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        print("LOGIN ERROR:", str(e))  # 🔥 important
        return Response(
            {"message": "Server error in login"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# =========================
# 🆕 SIGNUP API (FIXED)
# =========================

@api_view(['POST'])
def signup_view(request):
    try:
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        if not name or not email or not password:
            return Response(
                {"message": "All fields required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"message": "User already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ create user
        user = User.objects.create(
            name=name,
            email=email,
            password=make_password(password)
        )

        return Response(
            {"message": "Signup successful"},
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        print("SIGNUP ERROR:", str(e))  
        return Response(
            {"message": "Server error in signup"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        dropdown_id = self.request.query_params.get('dropdown_id')

        if dropdown_id:
            queryset = queryset.filter(dropdown_id=dropdown_id)

        return queryset


class CardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        section_id = self.request.query_params.get('section_id')

        if section_id:
            queryset = queryset.filter(section_id=section_id)

        return queryset