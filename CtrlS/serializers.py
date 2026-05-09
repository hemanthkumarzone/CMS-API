from rest_framework import serializers
from .models import *



class PortfolioDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioData
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class DropdownItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DropdownItem
        fields = '__all__'

class NavbarSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)
    dropdowns = DropdownItemSerializer(many=True, read_only=True)

    class Meta:
        model = Navbar
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']


class HeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hero
        fields = '__all__'


class InfrastructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfrastructureCard
        fields = '__all__'


class VisibilityCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisibilityCard
        fields = '__all__'


class VisibilitySerializer(serializers.ModelSerializer):
    cards = VisibilityCardSerializer(many=True, read_only=True)

    class Meta:
        model = Visibility
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


# ✅ FIXED FORM SERIALIZER
class DemoFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoForm
        fields = '__all__'

    def to_representation(self, instance):
        return {
            "title": "Request a Demo",  # ✅ ADD THIS (IMPORTANT)
            "name": instance.name_label,
            "email": instance.email_label,
            "organization": instance.organization_label,
            "source": instance.source_label,
            "submit": instance.submit_text,
        }


# ✅ FIXED MAIN DEMO SERIALIZER
class DemoSerializer(serializers.ModelSerializer):
    form = DemoFormSerializer(read_only=True)

    class Meta:
        model = Demo
        fields = '__all__'

class DemoFormSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoFormSubmission
        fields = '__all__'

class FooterItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterItem
        fields = '__all__'


class FooterSectionSerializer(serializers.ModelSerializer):
    items = FooterItemSerializer(many=True, read_only=True)

    class Meta:
        model = FooterSection
        fields = '__all__'


class FooterSerializer(serializers.ModelSerializer):
    sections = FooterSectionSerializer(many=True, read_only=True)

    class Meta:
        model = Footer
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
class BlogContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogContent
        fields = [
            'main_content',
            'sidebar_items',
            'demo_title',
            'demo_description'
        ]

class CardSerializer(serializers.ModelSerializer):
    content = BlogContentSerializer(read_only=True)

    class Meta:
        model = Card
        fields = [
            'id',
            'title',
            'description',
            'image',
            'slug',
            'is_featured',   # ✅ ADD
            'file',
            'created_at',
            'content'        # ✅ ADD (MOST IMPORTANT)
        ]

class SectionSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'title', 'description', 'dropdown', 'cards']


