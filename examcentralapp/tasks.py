from celery.decorators import task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from celery.task.schedules import crontab
from celery.decorators import periodic_task

from .utils import check_exam_start_date

logger = get_task_logger(__name__)

@task(name="send_email_task")
def send_email_task(to, subject, message):
    """sends an email when feedback form is filled successfully"""
    logger.info("Sent email")
    #email = EmailMessage(
    #            subject, message, to=to
    #)
    email = EmailMultiAlternatives(subject, message, "support@quizbuzz.in", to, reply_to=["noreply@quizbuzz.in"])
    email.content_subtype = 'html'  # Main content is text/html  
    email.mixed_subtype = 'related'  # This is critical, otherwise images will be displayed as attachments!
    return email.send()

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_publish_exam",
    ignore_result=True
)
def task_publish_exam():
    """
    Check for exam to be published
    """
    check_exam_start_date()
    logger.info("Checked for exams to publish.")
