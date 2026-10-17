import copy
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.staticfiles import finders
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import ContactForm
from .projects_data import PAGE_INTRO, PROJECTS, SECTIONS

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'home.html')


def Aboutme(request):
    return render(request, 'Aboutme.html')


def services(request):
    return render(request, 'services.html')


# ---------------------------------------------------------------------------
# Projects page (one page, three sections; content lives in projects_data.py)
# ---------------------------------------------------------------------------

def projects(request):
    sections = []
    for sec in SECTIONS:
        items = copy.deepcopy(PROJECTS.get(sec['key'], []))
        for p in items:
            # Only show the <video> player if the file actually exists in static/
            p['video_available'] = bool(p.get('video')) and finders.find(p['video']) is not None
        sections.append({**sec, 'projects': items})
    return render(request, 'projects.html', {
        'page_intro': PAGE_INTRO,
        'sections': sections,
    })


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject'] or f"New message from {name}"
            message = form.cleaned_data['message']

            full_message = f"From: {name} ({email})\n\n{message}"

            try:
                send_mail(
                    subject=subject,
                    message=full_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_RECEIVER_EMAIL],
                    fail_silently=False,
                )
            except Exception:
                logger.exception("Contact form email failed")
                messages.error(
                    request,
                    "Sorry, your message could not be sent. "
                    "Please email me directly at atsienookutse@gmail.com.",
                )
            else:
                messages.success(request, "Thank you! Your message has been sent. I'll get back to you shortly.")
                return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
