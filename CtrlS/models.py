from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class PortfolioData(models.Model):
    name = models.CharField(max_length=100)
    data = models.JSONField()

    def __str__(self):
        return self.name


class Navbar(models.Model):
    contact_button = models.CharField(max_length=100)
    demo_button = models.CharField(max_length=100)

    def __str__(self):
        return f"Navbar {self.id}"


class MenuItem(models.Model):
    navbar = models.ForeignKey(Navbar, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DropdownItem(models.Model):
    TYPE_CHOICES = (
        ('services', 'Services'), 
        ('resources', 'Resources'),
        ('platform', 'Platform'),
        ('company', 'Company'),
        ('get_started', 'Get Started'),
    )

    navbar = models.ForeignKey(Navbar, on_delete=models.CASCADE, related_name='dropdowns')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = RichTextField(blank=True, null=True)
    path = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.type} - {self.title}"
    



class Hero(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField()

    def __str__(self):
        return self.title


class InfrastructureCard(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField()

    def __str__(self):
        return self.title


class Visibility(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField()

    def __str__(self):
        return self.title


class VisibilityCard(models.Model):
    visibility = models.ForeignKey(Visibility, on_delete=models.CASCADE, related_name='cards')
    icon = models.CharField(max_length=200)
    title = models.CharField(max_length=255)
    description = RichTextField()

    def __str__(self):
        return self.title


class Service(models.Model):
    icon_type = models.CharField(max_length=50)
    icon = models.CharField(max_length=200)
    title = models.CharField(max_length=255)
    description = RichTextField()

    def __str__(self):
        return self.title


class Demo(models.Model):
    heading = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = RichTextField()

    def __str__(self):
        return self.title


class DemoForm(models.Model):
    demo = models.OneToOneField(Demo, on_delete=models.CASCADE, related_name='form')
    name_label = models.CharField(max_length=100)
    email_label = models.CharField(max_length=100)
    organization_label = models.CharField(max_length=100)
    source_label = models.CharField(max_length=100)
    submit_text = models.CharField(max_length=100)

    def __str__(self):
        return f"Form for {self.demo.title}"

class DemoFormSubmission(models.Model):
    demo = models.ForeignKey(Demo, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    email = models.EmailField()
    organization = models.CharField(max_length=100)
    source = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Footer(models.Model):
    tagline = RichTextField()
    description = RichTextField()
    copyright = models.CharField(max_length=255)

    def __str__(self):
        return "Footer"


class FooterSection(models.Model):
    footer = models.ForeignKey(
        Footer,
        on_delete=models.CASCADE,
        related_name="sections"   # ✅ IMPORTANT
    )
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class FooterItem(models.Model):
    section = models.ForeignKey(
        FooterSection,
        on_delete=models.CASCADE,
        related_name="items"
    )
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=200, blank=True, null=True)  # ✅ ADD THIS

    def __str__(self):
        return self.name
    
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
class Section(models.Model):
    dropdown = models.ForeignKey(
        DropdownItem,
        on_delete=models.CASCADE,
        related_name='sections'
    )
    title = models.CharField(max_length=200, blank=True, null=True)
    description = RichTextField(blank=True, null=True)

    def __str__(self):
        return f"{self.dropdown.title} - {self.title}"
    
class Card(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='cards')

    title = models.CharField(max_length=255)
    description = models.TextField()

    image = models.ImageField(upload_to='blogs/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class BlogContent(models.Model):
    card = models.OneToOneField(Card, on_delete=models.CASCADE, related_name="content")

    main_content = RichTextField(blank=True, null=True)   # ✅ FIXED

    sidebar_items = models.JSONField(default=list, blank=True)

    demo_title = models.CharField(max_length=255, blank=True, null=True)
    demo_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Content for {self.card.title}"
