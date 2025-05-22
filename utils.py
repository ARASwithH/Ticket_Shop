from django.contrib.sites import requests
from events.models import Event
from django.urls import reverse



def send_otp(phone_num, code):
    print(phone_num, code)
    pass


def send_reminder(ticket):
    print(ticket)
    pass



def send_rating_sms(users_phone_num):
    domain = '127.0.0.1:8000'

    for event, phone_nums in users_phone_num.items():
        event = Event.objects.get(name=event)
        url = reverse('events:rating-page', kwargs={'pk': event.id})
        full_url = f"{domain}{url}"
        for phone_num in phone_nums:
            print(
            f"Dear user, we appreciate your attention at the {event}. "
            f"You can rate the event if you would like to! Just click the link below:\n"
            f"{full_url}\n\n"
            f"Details:\nUser nums: {phone_num}, Event: {event}"
            )

        event.rated = True
        event.save()
