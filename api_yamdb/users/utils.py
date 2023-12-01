from django.core.mail import send_mail


def send_conf_code_mail(email, confirmation_code):
    send_mail(
        'Your confirmation code.',
        f'Your code to get JWT token is {confirmation_code}',
        'admin@yamdb.ru',
        [email],
    )
