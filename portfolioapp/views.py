import copy
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage
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

SUCCESS_MESSAGE = "Thank you! Your message has been sent. I'll get back to you shortly."


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Honeypot: a real visitor never sees this field, so any text means a bot.
            # Pretend it worked (so the bot doesn't adapt) but send nothing.
            if form.cleaned_data.get('website'):
                messages.success(request, SUCCESS_MESSAGE)
                return redirect('contact')

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject'] or f"New message from {name}"
            message = form.cleaned_data['message']

            full_message = f"From: {name} ({email})\n\n{message}"

            try:
                EmailMessage(
                    subject=subject,
                    body=full_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.CONTACT_RECEIVER_EMAIL],
                    reply_to=[email],               # pressing Reply writes to the visitor
                ).send(fail_silently=False)
            except Exception:
                logger.exception("Contact form email failed")
                messages.error(
                    request,
                    "Sorry, your message could not be sent. "
                    "Please email me directly at atsienookutse@gmail.com.",
                )
            else:
                messages.success(request, SUCCESS_MESSAGE)
                return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})