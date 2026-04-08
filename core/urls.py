from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('events/', views.events, name='events'),
    path('sermons/', views.sermons, name='sermons'),
    path('testimonies/', views.testimonies, name='testimonies'),

    # BLOGS – using primary key (pk) because slug removed
    path('blogs/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),   # <-- changed from <slug:slug>

    # APPOINTMENT / CONTACT
    path('appointment/', views.appointment, name='appointment'),
    path('contact/', views.contact, name='contact'),

    # MISC PAGES
    path('manchester/', views.manchester, name='manchester'),
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
    path('prayer-request/', views.prayer_request, name='prayer_request'),

    # TESTIMONY SUBMISSION
    path('test/', views.test, name='test'),

    # DONATIONS
    path('donate/', views.donate, name='donate'),
    path('donate/process/', views.process_donation, name='process_donation'),
    path('donation/success/', views.donation_success, name='donation_success'),
    path('donation/cancel/', views.donation_cancel, name='donation_cancel'),

    # DEBUG
    path('debug-images/', views.debug_images, name='debug_images'),

    path('create-admin/', views.create_admin, name='create_admin'),
]