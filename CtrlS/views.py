from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SectionSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.save()

            # =========================
            # 📩 EMAIL TO MENTOR
            # =========================
            send_mail(
                subject="New Demo Request 🚀",
                message=f"""
New Demo Request Received:

Name: {instance.name}
Email: {instance.email}
Organization: {instance.organization}
Source: {instance.source}
                """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.MENTOR_EMAIL],  # 🔥 CHANGE THIS
                fail_silently=False,
            )

            # =========================
            # 📩 EMAIL TO USER
            # =========================
            send_mail(
                subject="Thanks for requesting a demo 🎉",
                message=f"""
Hi {instance.name},

Thank you for your interest in CtrlS.

Our team has received your request and will contact you shortly.

Regards,  
CtrlS Team
                """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[instance.email],
                fail_silently=False,
            )

            return Response(
                {"message": "Demo request submitted successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   


class PortfolioDataViewSet(viewsets.ModelViewSet):
    queryset = PortfolioData.objects.all()
    serializer_class = PortfolioDataSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.save()

        # =========================
        # 📩 EMAIL TO ADMIN (KEEP THIS)
        # =========================
        send_mail(
            subject="New Contact Message 📩",
            message=f"""
New Contact Message Received:

Name: {instance.first_name} {instance.last_name}
Email: {instance.email}
Phone: {instance.phone}
Company: {instance.company}
Position: {instance.position}
Location: {instance.location}
City: {instance.city}
Inquiry: {instance.inquiry_type}

Message:
{instance.message}
            """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.MENTOR_EMAIL],
            fail_silently=False,
        )

        # =========================
        # 📩 HTML EMAIL TO USER (FIXED)
        # =========================
        html_content = render_to_string(
            "emails/welcome_email.html",
            {
                "name": instance.first_name
            }
        )

        text_content = strip_tags(html_content)

        email_msg = EmailMultiAlternatives(
            subject="We received your message 🎉",
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[instance.email],
        )

        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send()

        return Response(
            {"message": "Contact submitted successfully"},
            status=status.HTTP_201_CREATED
        )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
            return Response({"message": "All fields required"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"message": "User already exists"}, status=400)

        # ✅ Create user
        user = User.objects.create(
            name=name,
            email=email,
            password=make_password(password)
        )

        # =========================
        # 📩 HTML EMAIL
        # =========================

        html_content = render_to_string(
            "emails/welcome_email.html",
            {"name": name}
        )

        text_content = strip_tags(html_content)

        email_msg = EmailMultiAlternatives(
            subject="Welcome to AI FinOps 🎉",
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
        )

        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send()

        return Response({"message": "Signup successful"}, status=201)

    except Exception as e:
        print("ERROR:", str(e))
        return Response({"message": "Server error"}, status=500)
    
class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Section.objects.prefetch_related('cards__content').all()
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
from rest_framework.views import APIView


class BlogPageView(APIView):
    def get(self, request):
        sections = Section.objects.prefetch_related('cards__content').all()
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data)
    
class BlogDetailView(APIView):
    def get(self, request, slug):
        try:
            card = Card.objects.select_related('content').get(slug=slug)
            serializer = CardSerializer(card)
            return Response(serializer.data)
        except Card.DoesNotExist:
            return Response({"message": "Blog not found"}, status=404)