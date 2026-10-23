from celery import Celery
import src.config as conf
from src.mail import mail, create_message
from asgiref.sync import async_to_sync
c_app = Celery("bookly", broker= conf.broker_url, backend = conf.result_backend)

c_app.config_from_object('src.config')

@c_app.task()
def send_email(reciepents : list[str], subject: str, body:str):
    message = create_message(
            recipients=reciepents,
            subject = subject,
            body = body
        )
        
    async_to_sync(mail.send_message)(message)
    print("Email sent")