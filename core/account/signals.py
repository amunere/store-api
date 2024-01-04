from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import mail_managers, EmailMultiAlternatives
from .models import User
from django.template.loader import render_to_string
from django.conf import settings


"""
Notify the manager by email about the creation of a new user
"""
@receiver(post_save, sender=User)
def notify_managers(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.username}, {instance.email}'
    else:
        subject = f'Post changed for {instance.username}, {instance.email}'

    mail_managers(
        subject=subject,
        message=instance.email,
    )

"""
Notify the user by email about account creation
"""
@receiver(post_save, sender=User)
def notify_user(sender, instance, created, **kwargs):
    if created:        
        html_content = render_to_string(
            'mail.html',
            {
                # 'link': f'{settings.SITE_URL}',
                'instance': instance,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'Hi, {instance.username}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[instance.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()