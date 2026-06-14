from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    SectionViewSet,
    NavbarViewSet,
    MenuItemViewSet,
    DropdownItemViewSet,
    HeroViewSet,
    InfrastructureViewSet,
    VisibilityViewSet,
    VisibilityCardViewSet,
    ServiceViewSet,
    FooterViewSet,
    FooterSectionViewSet,
    FooterItemViewSet,
    DemoViewSet,
    DemoFormViewSet,
    DemoFormSubmissionViewSet,
    PortfolioDataViewSet,
    ContactViewSet,
    CardViewSet,
    login_view,
    signup_view,
    confirm_booking,
    booked_slots, 
    cancel_booking,
    booking_details,
    reschedule_booking,
    test_odoo
)

router = DefaultRouter()

# READ APIs
router.register(r'navbar', NavbarViewSet)
router.register(r'menu-items', MenuItemViewSet)
router.register(r'dropdowns', DropdownItemViewSet)
router.register(r'hero', HeroViewSet)
router.register(r'infrastructure', InfrastructureViewSet)
router.register(r'visibility', VisibilityViewSet)
router.register(r'visibility-cards', VisibilityCardViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'footer', FooterViewSet)
router.register(r'footer-sections', FooterSectionViewSet)
router.register(r'footer-items', FooterItemViewSet)
router.register(r"sections", SectionViewSet, basename="sections")

# CRUD APIs
router.register(r'demo', DemoViewSet)
router.register(r'demo-form', DemoFormViewSet)
router.register(r'demo-submit', DemoFormSubmissionViewSet)
router.register(r'portfolio', PortfolioDataViewSet)
router.register(r'contact', ContactViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'cards', CardViewSet)


urlpatterns = router.urls + [

    path('login/', login_view),

    path('signup/', signup_view),

    path("confirm-demo/", confirm_booking),

    path("booked-slots/", booked_slots),

    path(
    "cancel-booking/<uuid:token>/",
    cancel_booking
),

    path(
    "booking-details/<uuid:token>/",
    booking_details
),

    path(
    "reschedule-booking/<uuid:token>/",
    reschedule_booking
),
    path("test-odoo/", test_odoo),
]
 