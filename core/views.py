from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse

from .models import (
    ContactMessage,
    Appointment,
    Testimony,
    Event,
    Sermon,
    BlogPost,
    NewsletterSubscriber,
    Donation,
    PrayerRequest   # already imported here
)

# =========================
# CONTACT VIEW
# =========================
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            try:
                send_mail(
                    subject=f"Contact Form: {subject}",
                    message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except:
                pass

            messages.success(request, "Message sent successfully 🙌")
            return redirect('contact')

        messages.error(request, "Please fill in all fields.")

    return render(request, 'contact.html')


# =========================
# APPOINTMENT VIEW
# =========================
def appointment(request):
    if request.method == 'POST':
        Appointment.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            appointment_type=request.POST.get('appointment_type'),
            preferred_date=request.POST.get('preferred_date'),
            preferred_time=request.POST.get('preferred_time'),
            message=request.POST.get('message')
        )

        messages.success(request, "Appointment request submitted 🙏")
        return redirect('appointment')

    return render(request, 'appointment.html')


# =========================
# TESTIMONY SUBMISSION
# =========================
def test(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')

        if name and content:
            Testimony.objects.create(
                name=name,
                location=request.POST.get('location'),
                content=content,
                image=request.FILES.get('image')
            )

            messages.success(request, "Testimony submitted for review 🙏")
            return redirect('test')

        messages.error(request, "Name and testimony are required.")

    return render(request, 'test.html')


# =========================
# TESTIMONIES PAGE
# =========================
def testimonies(request):
    data = Testimony.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'testimonies.html', {'testimonies': data})


# =========================
# HOME PAGE
# =========================
def index(request):
    latest_sermons = Sermon.objects.all().order_by('-date')[:4]
    latest_posts = BlogPost.objects.filter(is_published=True).order_by('-date')[:3]
    latest_events = Event.objects.filter(is_upcoming=True).order_by('start_date')[:3]

    return render(request, 'index.html', {
        'latest_sermons': latest_sermons,
        'latest_posts': latest_posts,
        'latest_events': latest_events,
    })


# =========================
# STATIC PAGES
# =========================
def about(request):
    return render(request, 'about.html')

def manchester(request):
    return render(request, 'manchester.html')

# No duplicate import here – PrayerRequest already imported at top
def prayer_request(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if name and email and message:
            PrayerRequest.objects.create(name=name, email=email, message=message)
            messages.success(request, "Your prayer request has been submitted. We will pray for you.")
        else:
            messages.error(request, "Please fill in all fields.")
        return redirect('index')
    # If someone visits the URL directly (GET), redirect to home
    return redirect('index')

# =========================
# EVENTS
# =========================
def events(request):
    events = Event.objects.all().order_by('start_date')
    return render(request, 'events.html', {'events': events})


# =========================
# SERMONS
# =========================
def sermons(request):
    sermons = Sermon.objects.all().order_by('-date')
    return render(request, 'sermons.html', {'sermons': sermons})


# =========================
# BLOG LIST
# =========================
def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-date')
    return render(request, 'blog_list.html', {'posts': posts})


# =========================
# BLOG DETAIL – using primary key (pk)
# =========================
def blog_detail(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk, is_published=True)
    return render(request, 'blog_detail.html', {'blog': blog})


# =========================
# NEWSLETTER
# =========================
from .models import NewsletterSubscriber, Newsletter  # make sure Newsletter is included

def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            if not NewsletterSubscriber.objects.filter(email=email).exists():
                NewsletterSubscriber.objects.create(email=email)
                messages.success(request, "Subscribed successfully 🙌")
            else:
                messages.info(request, "You’re already subscribed.")

            return redirect('newsletter_signup')

        messages.error(request, "Enter a valid email.")

    newsletters = Newsletter.objects.filter(is_published=True).order_by('-created_at')

    return render(request, 'newsletter_signup.html', {
        'newsletters': newsletters
    })
# =========================
# DEBUG IMAGES
# =========================
def debug_images(request):
    events = Event.objects.all()
    html = "<h1>Event Images</h1><ul>"

    for e in events:
        if e.image:
            html += f"<li>{e.title}: {e.image.url}</li>"
        else:
            html += f"<li>{e.title}: no image</li>"

    html += "</ul>"
    return HttpResponse(html)


# =========================
# DONATION SYSTEM
# =========================
def donate(request):
    return render(request, 'donate.html')


def process_donation(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        currency = request.POST.get('currency', 'GBP')  # Get currency from form, default GBP

        if name and email and amount:
            donation = Donation.objects.create(
                name=name,
                email=email,
                amount=amount,
                status='pending'
            )

            paypal_url = "https://www.paypal.com/cgi-bin/webscr"
            invoice = f"PPN-{donation.id}"

            return redirect(
                f"{paypal_url}?cmd=_donations"
                f"&business=payments@prayerpowernetwork.org.uk"
                f"&currency_code={currency}"
                f"&amount={amount}"
                f"&item_name=Donation+to+Prayer+Power+Network"
                f"&invoice={invoice}"
                f"&return={request.build_absolute_uri('/donation/success/')}"
                f"&cancel_return={request.build_absolute_uri('/donation/cancel/')}"
            )

        messages.error(request, "Please fill in all fields.")
        return redirect('donate')

    return redirect('donate')


def donation_success(request):
    messages.success(request, "Thank you for your donation! God bless you.")
    return render(request, 'donation_status.html', {'status': 'success'})


def donation_cancel(request):
    messages.warning(request, "Donation cancelled. Please try again.")
    return render(request, 'donation_status.html', {'status': 'cancel'})


def regular(request):
    return render(request, 'regular.html')

def testimony_detail(request, pk):
    testimony = get_object_or_404(Testimony, pk=pk, is_approved=True)
    return render(request, 'testimony_detail.html', {'testimony': testimony})
# =========================
# CREATE ADMIN (TEMPORARY)
# =========================
from django.http import HttpResponse
from django.contrib.auth import get_user_model

def create_admin(request):
    User = get_user_model()
    if not User.objects.filter(username='prayer').exists():
        User.objects.create_superuser('prayer', 'media@prayerpowernetwork.org.uk', 'PrayerPowerNetwork_2026')
        return HttpResponse("Admin created: username=prayer, password=PrayerPowerNetwork_2026")
    return HttpResponse("Admin already exists")


# =========================
# CLOUDINARY DEBUG (TEMPORARY)
# =========================
from django.http import HttpResponse
from django.core.files.storage import default_storage
import os

def debug_cloudinary(request):
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', 'NOT SET')
    api_key = os.environ.get('CLOUDINARY_API_KEY', 'NOT SET')
    api_secret = os.environ.get('CLOUDINARY_API_SECRET', 'NOT SET')
    cloudinary_url = os.environ.get('CLOUDINARY_URL', 'NOT SET')
    storage_class = str(default_storage.__class__)
    
    html = f"""
    <h2>Cloudinary Debug Info</h2>
    <ul>
        <li><b>CLOUDINARY_CLOUD_NAME:</b> {cloud_name}</li>
        <li><b>CLOUDINARY_API_KEY:</b> {api_key}</li>
        <li><b>CLOUDINARY_API_SECRET:</b> {api_secret[:5]}... (truncated)</li>
        <li><b>CLOUDINARY_URL:</b> {cloudinary_url[:40] if cloudinary_url != 'NOT SET' else 'NOT SET'}</li>
        <li><b>Default Storage Class:</b> {storage_class}</li>
    </ul>
    """
    return HttpResponse(html)