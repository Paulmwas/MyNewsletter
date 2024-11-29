from django.shortcuts import render
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def home(request):
    saved_contacts = Contact.objects.all()

    if request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')

        if email:
            # Check if the email already exists in the database
            if Contact.objects.filter(email=email).exists():
                messages.error(request, email + " already exists.")
            else:
                contact = Contact(name=name, email=email)
                contact.save()
                messages.success(request, email + " has been added successfully.")
        else:
            print("No email provided")

    return render(request, 'home.html', {'saved_contacts': saved_contacts})


def send_mail_page(request):
    context = {}

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if subject and message:
            try:
                # Get email addresses from the Contact model
                email_addresses = Contact.objects.values_list('email', flat=True)

                # Send the email
                send_mail(subject, message, settings.EMAIL_HOST_USER, email_addresses)

                context['result'] = 'Emails sent successfully'
            except Exception as e:
                context['result'] = f'Error sending emails: {e}'
        else:
            context['result'] = 'All fields are required'

    return render(request, "messenger.html", context)
