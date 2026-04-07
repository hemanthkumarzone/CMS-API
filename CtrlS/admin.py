from django.contrib import admin
from .models import (
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