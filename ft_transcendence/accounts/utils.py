import random
from django.core.mail import EmailMessage
from .models import User, OneTimePassword
from django.conf import settings

def generateOtp():
	otp=""
	for i in range(6):
		otp += str(random.randint(1, 9))
	return otp



def send_code_to_user(email):
	Subject="One time passcode for Email verification"
	otp_code=generateOtp()
	user=User.objects.get(email=email)
	current_site="deciding-delicate-raptor.ngrok-free.app"
	email_body=f"Hi {user.first_name} thanks for signing up on {current_site} \
		Please verify your email with the one time passcode {otp_code}"
	from_email=settings.DEFAULT_FROM_EMAIL	
	OneTimePassword.objects.create(user=user, code=otp_code)
	send_email=EmailMessage(subject=Subject, body=email_body,
					from_email=from_email, to=[email])
	send_email.send(fail_silently=False)
