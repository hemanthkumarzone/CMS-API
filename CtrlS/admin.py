from django.contrib import admin
from .models import (
    Contact,
    DemoFormSubmission,
    PortfolioData,
    Navbar, MenuItem, DropdownItem,
    Hero,
    InfrastructureCard,
    Visibility, VisibilityCard,
    Service,
    Demo, DemoForm,
    Footer,
    FooterSection, FooterItem
)
from .models import Section, Card
from .models import BlogContent

admin.site.register(PortfolioData)
admin.site.register(Navbar)
admin.site.register(MenuItem)
admin.site.register(DropdownItem)
admin.site.register(Hero)
admin.site.register(InfrastructureCard)
admin.site.register(Visibility)
admin.site.register(VisibilityCard)
admin.site.register(Service)
admin.site.register(Demo)
admin.site.register(DemoForm)
admin.site.register(Footer)
admin.site.register(FooterSection)
admin.site.register(FooterItem)
admin.site.register(Section)
admin.site.register(Card)
admin.site.register(BlogContent)
admin.site.register(DemoFormSubmission)
admin.site.register(Contact)