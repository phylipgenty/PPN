from django.contrib import admin
from .models import (
    ContactMessage,
    Appointment,
    Testimony,
    NewsletterSubscriber,
    Event,
    Sermon,
    BlogPost
)

# CONTACT MESSAGES
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"


# APPOINTMENTS
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'phone',
        'appointment_type',
        'preferred_date', 'preferred_time',
        'is_processed'
    )
    list_filter = ('appointment_type', 'is_processed', 'preferred_date')
    search_fields = ('name', 'email', 'phone')


# TESTIMONIES
@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('name', 'location', 'content')
    actions = ['approve_testimonies']

    def approve_testimonies(self, request, queryset):
        queryset.update(is_approved=True)
    approve_testimonies.short_description = "Approve selected testimonies"


# NEWSLETTER SUBSCRIBERS
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)


# EVENTS
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'location', 'is_upcoming')
    list_filter = ('is_upcoming', 'start_date')
    search_fields = ('title', 'location')


# SERMONS
@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'preacher', 'date')
    list_filter = ('date',)
    search_fields = ('title', 'preacher')


# BLOG POSTS – No slug, no image_url, only file upload
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'is_published')
    list_filter = ('is_published', 'date')
    search_fields = ('title', 'content')
    fields = ('title', 'image', 'content', 'author', 'is_published')   # removed 'date'