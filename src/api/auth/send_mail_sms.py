from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_otp_email(user_email, otp_code, otp_type='otp'):
    # 1. HTML tarkibni render qilish
    if otp_type == "otp":
        context = {'code': otp_code}
        html_message = render_to_string('verify_email.html', context)
    else:
        context = {'link': otp_code}
        html_message = render_to_string('verify_email_link.html', context)
    # 2. Plain text varianti (HTML qo'llab-quvvatlamaydigan pochta xizmatlari uchun)
    plain_message = strip_tags(html_message)
    subject = f"Tasdiqlash kodi"
    # Fall back to DEFAULT_FROM_EMAIL if EMAIL_HOST_USER is not configured.
    from_email = settings.EMAIL_HOST_USER or settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    # 3. Send. Do NOT swallow errors: a failed send must propagate so the caller
    #    can report a real error instead of a false "code sent" success.
    send_mail(
        subject,
        plain_message,
        from_email,
        recipient_list,
        html_message=html_message,
        fail_silently=False,
    )
