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
from django.shortcuts import get_object_or_404


from .models import *
from .serializers import *

# JWT
import jwt
from datetime import datetime, timedelta
import uuid


# READ-ONLY APIs


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

            print("DEMO SUBMITTED:", instance.email)

            
            send_mail(
                subject="New Demo Request 🚀",
                message=f"""
Name: {instance.name}
Email: {instance.email}
Organization: {instance.organization}
Source: {instance.source}
                """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.MENTOR_EMAIL],
                fail_silently=False,
            )

            
            html_content = render_to_string(
                "emails/demo_request.html",
                {
                    "first_name": instance.name,
                    "company_name": instance.organization,
                    "product_name": "CtrlS",
                    "booking_link": "http://localhost:5173/book-demo"
                }
            )

            text_content = strip_tags(html_content)

            email_msg = EmailMultiAlternatives(
                subject="We received your demo request 🚀",
                body=text_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[instance.email],
            )

            email_msg.attach_alternative(html_content, "text/html")
            email_msg.send()

            print("EMAIL SENT")

            return Response({"message": "Demo submitted"}, status=201)

        return Response(serializer.errors, status=400)
   


class PortfolioDataViewSet(viewsets.ModelViewSet):
    queryset = PortfolioData.objects.all()
    serializer_class = PortfolioDataSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        instance = serializer.save()

       
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

        
        send_mail(
            subject="We received your message 🎉",
            message=f"""
Hi {instance.first_name},

Thank you for contacting CtrlS AI FinOps.

We have successfully received your message and our team will get back to you shortly.

----------------------------------------
Your Details:
Name: {instance.first_name} {instance.last_name}
Email: {instance.email}
Company: {instance.company}
----------------------------------------

Best regards,  
CtrlS Team
            """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=False,
        )

        return Response(
            {"message": "Contact submitted successfully"},
            status=status.HTTP_201_CREATED
        )


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

        
        user = User.objects.create(
            name=name,
            email=email,
            password=make_password(password)
        )

       
        html_content = render_to_string(
    "emails/welcome_email.html",
    {
        "name": name,
        "organization": "CTRLS",
        "plan": "Business Enterprise Plan",
        "admin_email": email
    }
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
        
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


@api_view(['POST'])
def confirm_booking(request):
    name = request.data.get("name")
    email = request.data.get("email")
    date = request.data.get("selected_date")
    time = request.data.get("selected_time")

    
    duration = "30 minutes"
    host = "CtrlS Team"
    meeting_id = str(uuid.uuid4())[:8]

    meeting_link = (
        f"https://meet.ctrls.com/demo-{meeting_id}"
    )
    
    passcode = "123456"

    print("BOOKING RECEIVED:", name, email, date, time)

    booking = DemoBooking.objects.create(

    name=name,

    email=email,

    linkedin=request.data.get("linkedin"),

    notes=request.data.get("notes"),

    selected_date=date,

    selected_time=time,

    timezone=request.data.get(
        "timezone",
        "Asia/Kolkata"
    ),

    google_meet_link=meeting_link,

    status="confirmed"
)
    cancel_url = (
    f"http://localhost:5173/"
    f"cancel-booking/"
    f"{booking.booking_token}"
)

    # EMAIL TEMPLATE
    html_content = render_to_string(
        "emails/demo_confirmation.html",
        {
            "first_name": name,
            "selected_date": date,
            "selected_time": time,
            "duration": duration,
            "host": host,
            "meeting_link": meeting_link,
            "passcode": passcode,
            "cancel_url": cancel_url,
        }
    )

    text_content = strip_tags(html_content)

    email_msg = EmailMultiAlternatives(
      subject="🎉 Your Demo is Confirmed",
      body=text_content,
      from_email=settings.EMAIL_HOST_USER,  
      to=[email],
)

    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send()

    return Response({

    "message": "Demo confirmed",

    "meeting_link": meeting_link,

    "cancel_url": cancel_url,

    "booking_id": str(
        booking.booking_token
    )

})

@api_view(['GET'])
def booked_slots(request):

    selected_date = request.GET.get("date")

    if not selected_date:

        return Response(
            {
                "error": "Date is required"
            },
            status=400
        )

    bookings = DemoBooking.objects.filter(
        selected_date=selected_date,
        status__in=["pending", "confirmed"]
    )

    slots = bookings.values_list(
        "selected_time",
        flat=True
    )

    return Response(
        {
            "booked_slots": list(slots)
        }
    )

@api_view(['GET'])
def cancel_booking(request, token):

    try:

        booking = DemoBooking.objects.get(
            booking_token=token
        )

        if booking.status == "cancelled":

            return Response({

                "message":
                "Booking already cancelled"

            })

        if booking.status == "completed":

            return Response({

                "message":
                "Completed bookings cannot be cancelled"

            })

        booking.status = "cancelled"

        booking.save()

        return Response({

            "success": True,

            "message":
            "Booking cancelled successfully"

        })

    except DemoBooking.DoesNotExist:

        return Response({

            "error":
            "Invalid booking token"

        }, status=404)
    
@api_view(['GET'])
def booking_details(request, token):

    try:

        booking = DemoBooking.objects.get(
            booking_token=token
        )

        return Response({

            "name": booking.name,

            "email": booking.email,

            "linkedin": booking.linkedin,

            "notes": booking.notes,

            "selected_date":
            booking.selected_date,

            "selected_time":
            booking.selected_time,

            "timezone":
            booking.timezone,

        })

    except DemoBooking.DoesNotExist:

        return Response({

            "error":
            "Booking not found"

        }, status=404)
    
@api_view(['PUT'])
def reschedule_booking(request, token):

    try:

        booking = DemoBooking.objects.get(
            booking_token=token
        )

        if booking.status == "cancelled":

            return Response({

                "message":
                "Cancelled bookings cannot be rescheduled"

            })

        booking.selected_date = (
            request.data.get(
                "selected_date"
            )
        )

        booking.selected_time = (
            request.data.get(
                "selected_time"
            )
        )

        booking.timezone = (
            request.data.get(
                "timezone",
                booking.timezone
            )
        )

        booking.save()

        return Response({

            "success": True,

            "message":
            "Booking rescheduled successfully"

        })

    except DemoBooking.DoesNotExist:

        return Response({

            "error":
            "Booking not found"

        }, status=404)