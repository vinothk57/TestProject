import os
from django.conf import settings
import datetime as DT
import re
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.template import RequestContext
from django.shortcuts import render_to_response
from examcentralapp.forms import *
from examcentralapp.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.utils import timezone

def check_exam_start_date():
    """
      Checks for Exam Start Date and Publish if required
    """

    examlist = []
    examlist = ExamName.objects.all()

    for exam in examlist:
        if exam.end_time > timezone.now():
            if exam.start_time < timezone.now():
                exam.published = True
                exam.save()
            elif exam.start_time > timezone.now():
                if exam.published == True:
                    exam.published = False
                    exam.save()
            else:
                pass
        elif exam.end_time < timezone.now():
            if exam.published == True:
                exam.published = False
                exam.save()
        else:
            pass
