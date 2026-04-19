from django.db import models
from cloudinary.models import CloudinaryField   # <-- ADD THIS

# Contact form messages
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject[:50]}"

    class Meta:
        ordering = ['-created_at']


# Appointment requests
class Appointment(models.Model):
    APPOINTMENT_TYPES = (
        ('prayer', 'Prayer Request'),
        ('counseling', 'Pastoral Counseling'),
        ('deliverance', 'Deliverance Session'),
        ('marriage', 'Marriage Counseling'),
        ('general', 'General Appointment'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPES, default='general')
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.preferred_date} {self.preferred_time}"

    class Meta:
        ordering = ['-created_at']


# Testimonies – image changed to CloudinaryField
class Testimony(models.Model):
    title = models.CharField(max_length=200, default="My Testimony")
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    image = CloudinaryField('image', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-created_at']


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-subscribed_at']


# =========================
# NEW NEWSLETTER MODEL
# =========================
class Newsletter(models.Model):
    title = models.CharField(max_length=200)
    cover_image = CloudinaryField('image', blank=True, null=True)   # optional cover image
    pdf_file = CloudinaryField('file', blank=True, null=True)       # PDF file
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


# Events – image changed to CloudinaryField
class Event(models.Model):
    title = models.CharField(max_length=200)
    image = CloudinaryField('image', blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200)
    description = models.TextField()
    is_upcoming = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_date']


# Sermons
class Sermon(models.Model):
    title = models.CharField(max_length=200)
    video_id = models.CharField(max_length=50, help_text="YouTube video ID (the part after v=)")
    preacher = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.preacher}"

    class Meta:
        ordering = ['-date']


# Blog Posts – image changed to CloudinaryField
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    image = CloudinaryField('image', blank=True, null=True)
    content = models.TextField()
    author = models.CharField(max_length=100, default="Pastor Henry Onyirioha")
    date = models.DateField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']


class Donation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    paypal_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - £{self.amount} - {self.status}"


class PrayerRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"