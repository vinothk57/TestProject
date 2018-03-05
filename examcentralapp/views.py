import os
from django.conf import settings
import datetime as DT
import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

# Create your views here.
from django.http import HttpResponse, Http404
from django.template import Context
from django.template.loader import get_template
from django.template.loader import *
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#For Reset password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.views.generic import *
from examcentralapp.forms import PasswordResetRequestForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.contrib.auth import get_user_model

from django.template.loader import render_to_string
from .token import account_activation_token
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage

import logging, traceback
import examcentralapp.constants as constants
import examcentralapp.config as config
import hashlib
from random import randint
from django.core.urlresolvers import reverse

def web_page(request):
    return render(request, 'web.html', {})

def main_page(request):
  
  if not request.user.is_authenticated():
    return render(request, 'index.html', {})

  current_page = int(request.GET.get('page' ,1))
  limit = 10 * current_page
  offset = limit - 10

  examlist = []
  if not request.user.is_staff:
      examlist = ExamName.objects.filter(published=True).order_by('-id')[offset:limit]
  else:
      examlist = ExamName.objects.all().order_by('-id')[offset:limit]

  total_list = ExamName.objects.filter(published=True).count()

  total_pages = int(total_list / 10)

  reminder = total_list % 10

  if reminder:
     total_pages += 1 # adding one more page if the last page will contains less contacts 

  pagination = make_pagination_html(current_page, total_pages)

  #variables = RequestContext(request, {'examlist': examlist})
  #return render_to_response(
  #  'main_page.html', variables
  #)
  form = SearchForm()
  
  show_results = True
  if 'query' in request.GET:
    show_results = True
    query = request.GET['query'].strip()
    if query:
      form = SearchForm({'query' : query}) 
      examlist = ExamName.objects.filter(examname__icontains=query)[:10]
    if 'blank' in request.GET:
      examlist = ExamName.objects.filter(published=True)
  variables = RequestContext(request, { 'form': form,
    'examlist': examlist,
    'show_results': show_results,
    'show_tags': True
  })

  if 'ajax' in request.GET:
    return render(request, 'examlist.html', { 'form': form,
    'examlist': examlist,
    'show_results': show_results,
    'show_tags': True
    })

  else:
    return render(request, 'home_page.html', { 'form': form,
    'examlist': examlist,
    'show_results': show_results,
    'show_tags': True,
    'pagination': pagination,
    'offset': offset
    })


def user_loggedin(request):
  if request.user.is_authenticated():
    username = request.user.username
  redirect_url = '/'
  #redirect_url = '/user/' + username
  return HttpResponseRedirect(redirect_url)

@login_required
def user_page(request, username):
  current_page = int(request.GET.get('page' ,1))
  limit = 10 * current_page
  offset = limit - 10

  user = get_object_or_404(User, username=username)
  exams = user.userexams_set.order_by('-id')[offset:limit]
  total_list = user.userexams_set.order_by('-id').count()

  total_pages = int(total_list / 10)

  reminder = total_list % 10

  if reminder:
     total_pages += 1 # adding one more page if the last page will contains less contacts 

  pagination = make_pagination_html(current_page, total_pages)


  userexams = []
  for exam in exams:
      detailsdict = {}
      detailsdict['examrec'] = exam

      uexamattemptinfo = UserExamAttemptInfo.objects.get(userexam_id=exam.id)
      max_attempts_for_user = uexamattemptinfo.attempt_available
      usedAttempts = UserScoreSheet.objects.filter(user_id=request.user.id,
                         examname_id=exam.examname.id
                          ).count()
      attemptsremaining = max_attempts_for_user - usedAttempts

      detailsdict['max_user_attempts'] = max_attempts_for_user
      detailsdict['rem_attempts'] = attemptsremaining

      userexams.append(detailsdict)


  variables = RequestContext(request, {
    'username': username,
    'userexams': exams,
    'show_tags': True
  })
  return render(request, 'user_page.html', {
    'username': username,
    'userexams': userexams,
    'show_tags': True,
    'pagination': pagination,
    'offset': offset
  })


@login_required
def profile_page(request):

  if request.method == 'POST':
    form = UpdateProfileForm(request.POST)
    if form.is_valid():
      user = User.objects.filter(username=form.cleaned_data['username']).update(first_name=form.cleaned_data['firstname'])
      user = User.objects.filter(username=form.cleaned_data['username']).update(last_name=form.cleaned_data['lastname'])

      try:
        UserDetails.objects.get(user_id=request.user.id)
      except ObjectDoesNotExist:
        userdetail, dummy = UserDetails.objects.get_or_create(
          user_id=request.user.id,
          address=form.cleaned_data['address'],
          city=form.cleaned_data['city'],
          country=form.cleaned_data['country'],
          pincode=form.cleaned_data['pincode'],
          aboutme=form.cleaned_data['aboutme']
        )
        return HttpResponseRedirect('/profile')
        
      userdetail = UserDetails.objects.filter(user_id=request.user.id).update(
                     address=form.cleaned_data['address'],
                     city=form.cleaned_data['city'],
                     country=form.cleaned_data['country'],
                     pincode=form.cleaned_data['pincode'],
                     aboutme=form.cleaned_data['aboutme']
                   )

      return HttpResponseRedirect('/profile')
    
  else:
    form = UpdateProfileForm()

  variables = RequestContext(request, {
                'form': form,
                'uid' : request.user.id
              })

  return render(request, 'profile.html', {
                'form': form,
                'uid' : request.user.id
              })


def logout_page(request):
  logout(request)
  messages.info(request, 'You have successfully logged out!')
  return HttpResponseRedirect('/')

def register_page(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      user = User.objects.create_user(
        username=form.cleaned_data['username'],
        first_name=form.cleaned_data['firstname'],
        last_name=form.cleaned_data['lastname'],
        password=form.cleaned_data['password1'],
        email=form.cleaned_data['email']
      )
      user.is_active = False
      user.save()
      #send_mail(
      #  'QuizBuzz - Account Registration',
      #  'Hi,\n\n\
      #   Your Email Id is registered with QuizBuzz.in.\n\
      #   Your Username: ' + form.cleaned_data['username'] + '\n\nThanks,\nQuizBuzz Team.',
      #  'from@example.com',
      #  [form.cleaned_data['email']],
      #  fail_silently=False,
      #)
      #return HttpResponseRedirect('/')
      
      mail_subject = 'Account Activation - QuizBuzz'
      message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': request.META['HTTP_HOST'],
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
      to_email = form.cleaned_data.get('email')
      email = EmailMessage(
                  mail_subject, message, to=[to_email]
      )
      email.send()
      messages.info(request, 'Please confirm your email address to complete the registration')
      return HttpResponseRedirect('/')
  else:
    form = RegistrationForm()

  variables = RequestContext(request, {
                 'form': form
              })

  return render(request, 'registration/register.html', { 'form': form })
  #return render_to_response(
  #  'registration/register.html', 
  #  variables
  #)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #login(request, user)
        # return redirect('home')
        #return HttpResponse('Thank you for your email confirmation. Now you can login to your QuizBuzz account.')
        messages.info(request, 'Thank you for your email confirmation. Now you can login to your QuizBuzz account.')
        return HttpResponseRedirect('/')
    else:
        messages.info(request, 'Activation link is invalid')
        return HttpResponseRedirect('/')

@login_required
def examdetails_save_page(request):
  if not request.user.is_staff:
      return HttpResponseRedirect('/')
  if request.method == 'POST':
    form = ExamDetailsSaveForm(request.POST)
    if form.is_valid():
      # Create or get Exam Detail.
      examname, created = ExamName.objects.get_or_create(
        examname=form.cleaned_data['examname'], total_questions=form.cleaned_data['total_questions'],
        attempts_allowed=form.cleaned_data['attempts_allowed'], duration=form.cleaned_data['duration'],
        start_time=form.cleaned_data['start_time'], end_time=form.cleaned_data['end_time'], mark_per_qtn=form.cleaned_data['mark_per_qtn'],
        negative_per_qtn=form.cleaned_data['neg_per_qtn'], price=form.cleaned_data['price'],
        published=False
      )

      # If the UserExam is being updated, clear old tag list.
      if not created:
        examname.tag_set.clear()
      # Create new tag list.
      tag_names = form.cleaned_data['tags'].split()
      for tag_name in tag_names:
        tag, dummy = Tag.objects.get_or_create(name=tag_name)
        examname.tag_set.add(tag)
      # Save examname to database.
      examname.save()
      form = QuestionDetailsSaveForm()
      variables =  RequestContext(request, {
                     'examname': examname.examname,
                     'examid': examname.id,
                     'quploaded': 0,
                     'form': form
                   })

      #return render(request, 'staff/addquestions.html', {
      #               'examname': examname.examname,
      #               'examid': examname.id,
      #               'quploaded': 0,
      #               'form': form
      #             })

      messages.info(request, 'Exam Created Successfully. Add Questions!')
      return HttpResponseRedirect('/')
  else:
    form = ExamDetailsSaveForm()
  variables = RequestContext(request, {
    'form': form
  })
  return render(request, 'staff/createexam.html',  {
    'form': form
  })


def search_page(request):
  form = SearchForm()
  examlist = []
  show_results = False
  if 'query' in request.GET:
    show_results = True
    query = request.GET['query'].strip()
    if query:
      form = SearchForm({'query' : query}) 
      examlist = ExamName.objects.filter(examname__icontains=query)[:10]
  if 'blank' in request.GET:
    examlist = ExamName.objects.filter(published=True)
  variables = { 'form': form,
    'form': form,
    'examlist': examlist,
    'show_results': show_results,
    'show_tags': True,
    'show_user': True
  }

  if 'ajax' in request.GET:
    return render(request, 'examlist.html', variables)
  else:
    return render(request, 'search.html', variables)

@login_required
def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.filter(id=request.user.id)

            if user.exists():
               try:
                 userdetail = UserDetails.objects.get(user_id=request.user.id)
               except ObjectDoesNotExist:
                 userdetail, dummy = UserDetails.objects.get_or_create(
                                       user_id=request.user.id
                                     )
               userdetail.profilepic = request.FILES['docfile']
               userdetail.save()
               return HttpResponseRedirect('/profile')
            return HttpResponseRedirect('/profile')
    else:
        form = DocumentForm()
        return render(request, 'model_form_upload.html', {
            'form': form
        })

@login_required
def addexam_page(request):
  if request.method == 'POST':
    #Create userexam
    userexam, created = UserExams.objects.get_or_create(
        user_id=request.user.id,
        examname_id=request.POST.get("examid", "")
    )

    examid = request.POST.get("examid","")
    attempts_per_purchase = ExamName.objects.get(id=examid).attempts_allowed

    if created:
        #create userexamattemptinfo with attempts per purchase from examname
        uexam_attempt, dummy = UserExamAttemptInfo.objects.get_or_create(
                userexam_id = userexam.id,
                attempt_available = attempts_per_purchase
            )
        messages.info(request, "Exam added to your account.")
        redirect_url = '/user/' + request.user.username
        return HttpResponseRedirect(redirect_url)
    else:
        #update userexamattemptinfo with additional attempts per purchase from examname
        uexamattemptinfo = UserExamAttemptInfo.objects.get(userexam_id=userexam.id)
        current_available_attempts = uexamattemptinfo.attempt_available
        new_attempts = attempts_per_purchase + current_available_attempts
        uexamattemptinfo.attempt_available = new_attempts
        uexamattemptinfo.save()

        messages.info(request, "Exam added to your account.")
        redirect_url = '/user/' + request.user.username
        return HttpResponseRedirect(redirect_url)

    messages.info(request, "Adding exam to account failed.")
    return HttpResponseRedirect('/myaccount')

@login_required
def removeexam_page(request):
  if request.method == 'POST':
      #Get userexam
      userexam = UserExams.objects.filter(
        user_id=request.user.id,
        examname_id=request.POST.get("examid", "")
      )
      if userexam.exists():
          userexam.delete()
  return HttpResponseRedirect('/myaccount')


@login_required
def addquestions_page(request):
  if request.method == 'POST':
    form = QuestionDetailsSaveForm(request.POST, request.FILES)
    if form.is_valid():
      right_options = ""
      # Add question
      examquestionobject = ExamQuestions.objects.filter(examname_id=request.POST.get("examid", ""), qno=form.cleaned_data['qno'])

      if examquestionobject.exists():
          examquestion = examquestionobject[0]
          examquestion.question = form.cleaned_data['question']
          examquestion.qtype = form.cleaned_data['qtype']
          examquestion.qcategory=form.cleaned_data['qcategory']
          examquestion.answer=form.cleaned_data['answer']
          examquestion.haspic = form.cleaned_data['haspic']
          examquestion.hasdirection=form.cleaned_data['hasdirection']
          examquestion.save()
      else:
          examquestion, created = ExamQuestions.objects.get_or_create(
            examname_id=request.POST.get("examid", ""), qno=form.cleaned_data['qno'], question=form.cleaned_data['question'],
            qtype=form.cleaned_data['qtype'], qcategory=form.cleaned_data['qcategory'], haspic=form.cleaned_data['haspic'],
            hasdirection=form.cleaned_data['hasdirection'], answer=form.cleaned_data['answer']
          )

      isOptionA = form.cleaned_data['isOptionA']
      optionAobject = OptionA.objects.filter(examname_id = request.POST.get("examid", ""), qid=form.cleaned_data['qno'])

      if optionAobject.exists():
          optionA = optionAobject[0]
          optionA.option = form.cleaned_data['optionA']
          optionA.isright = isOptionA
          optionA.save()
      else:
          optionA, created = OptionA.objects.get_or_create(
            examname_id = request.POST.get("examid", ""), qid=form.cleaned_data['qno'], option=form.cleaned_data['optionA'],
           isright = isOptionA
          )

      isOptionB = form.cleaned_data['isOptionB']
      optionBobject = OptionB.objects.filter(examname_id = request.POST.get("examid", ""), qid=form.cleaned_data['qno'])

      if optionBobject.exists():
          optionB = optionBobject[0]
          optionB.option = form.cleaned_data['optionB']
          optionB.isright = isOptionB
          optionB.save()
      else:
          optionB, created = OptionB.objects.get_or_create(
            examname_id = request.POST.get("examid", ""), qid=form.cleaned_data['qno'], option=form.cleaned_data['optionB'],
            isright = isOptionB
          )

      isOptionC = form.cleaned_data['isOptionC']
      optionCobject = OptionC.objects.filter(examname_id = request.POST.get("examid", ""), qid=form.cleaned_data['qno'])
      if request.POST.get("optionC", ""):
          if optionCobject.exists():
              optionC = optionCobject[0]
              optionC.option = form.cleaned_data['optionC']
              optionC.isright = isOptionC
              optionC.save()
          else:
              optionC, created = OptionC.objects.get_or_create(
                      examname_id = request.POST.get("examid", ""), qid=form.cleaned_data['qno'], option=form.cleaned_data['optionC'],
                      isright = isOptionC
                      )
      else:
          if optionCobject.exists():
              optionCobject.delete()

      isOptionD = form.cleaned_data['isOptionD']
      optionDobject = OptionD.objects.filter(examname_id = request.POST.get("examid", ""), qid=form.cleaned_data['qno'])
      if request.POST.get("optionD", ""):
          if optionDobject.exists():
              optionD = optionDobject[0]
              optionD.option = form.cleaned_data['optionD']
              optionD.isright = isOptionD
              optionD.save()
          else:
              optionD, created = OptionD.objects.get_or_create(
                      examname_id = request.POST.get("examid", ""), qid=form.cleaned_data['qno'], option=form.cleaned_data['optionD'],
                      isright = isOptionD
                      )
      else:
          if optionDobject.exists():
              optionDobject.delete()

      isOptionE = form.cleaned_data['isOptionE']
      optionEobject = OptionE.objects.filter(examname_id = request.POST.get("examid", ""), qid=form.cleaned_data['qno'])
      if request.POST.get("optionE", ""):
          if optionEobject.exists():
              optionE = optionEobject[0]
              optionE.option = form.cleaned_data['optionE']
              optionE.isright = isOptionE
              optionE.save()
          else:
              optionE, created = OptionE.objects.get_or_create(
                      examname_id = request.POST.get("examid", ""), qid=form.cleaned_data['qno'], option=form.cleaned_data['optionE'],
                      isright = isOptionE
                      )
      else:
          if optionEobject.exists():
              optionEobject.delete()

      if isOptionA:
        right_options += "1"
      if isOptionB:
        right_options += " 2"
      if isOptionC:
        right_options += " 3"
      if isOptionD:
        right_options += " 4"
      if isOptionE:
        right_options += " 5"

      qinfoObject = QuestionInfo.objects.filter(examname_id = request.POST.get("examid", ""), qid=form.cleaned_data['qno'])
      if qinfoObject.exists():
          qinfo = qinfoObject[0]

          if form.cleaned_data['haspic']:
              if qinfo.pic.name:
                  try:
                      os.remove(os.path.join(settings.MEDIA_ROOT, qinfo.pic.name))
                  except OSError:
                      messages.info(request, 'Error removing file')
                      pass
              if 'pic' in request.FILES:
                  qinfo.pic=request.FILES['pic']
                  qinfo.direction=form.cleaned_data['direction']
                  qinfo.save()
          elif form.cleaned_data['hasdirection']:
              if qinfo.pic.name:
                  try:
                      os.remove(os.path.join(settings.MEDIA_ROOT, qinfo.pic.name))
                  except OSError:
                      pass
              qinfo.pic.name=""
              qinfo.direction=form.cleaned_data['direction']
              qinfo.save()
          else:
              if qinfo.pic.name:
                  try:
                      os.remove(os.path.join(settings.MEDIA_ROOT, qinfo[0].pic.name))
                  except OSError:
                      pass
              qinfo.delete()
      #if no qinfo entry
      else:

          if form.cleaned_data['haspic'] or form.cleaned_data['hasdirection']:
              qinfo, created = QuestionInfo.objects.get_or_create(examname_id = request.POST.get("examid", ""), qid=form.cleaned_data['qno'],
                                                              direction=form.cleaned_data['direction']
                                                            )
              
              if form.cleaned_data['haspic']:
                  qinfo.pic=request.FILES['pic']
                  qinfo.save()

      solutionobject = ExamSolution.objects.filter(examname_id = request.POST.get("examid", ""), qid=form.cleaned_data['qno'])

      if solutionobject.exists():
          solution = solutionobject[0]
          solution.correct_options = right_options
          solution.explanation = form.cleaned_data['answer']
          solution.save()
      else:
          solution, created = ExamSolution.objects.get_or_create(examname_id = request.POST.get("examid", ""), qid=form.cleaned_data['qno'],
                                                             correct_options = right_options, explanation = form.cleaned_data['answer']
                                                            )

      examname = ExamName.objects.get(id=request.POST.get("examid", "")).examname
      uploaded_questions = ExamQuestions.objects.filter(examname_id=request.POST.get("examid", "")).count()
      form = QuestionDetailsSaveForm()
      variables =  {
                     'examname': examname,
                     'examid': request.POST.get("examid", ""),
                     'quploaded': uploaded_questions,
                     'form': form
                   }

      #return render(request, 'addquestions.html', variables)
      messages.info(request, 'Question added successfully!')
      exam = ExamName.objects.get(id=request.POST.get('examid', ""))
      totalqtns = ExamName.objects.get(id=request.POST.get('examid', "")).total_questions

      qlist = ExamQuestions.objects.filter(examname_id=request.POST.get('examid', "")).order_by('qno')
      return render(request, 'staff/examdetails.html', {
            'examid': request.POST.get('examid', ""),
            'examname': exam.examname,
            'totalqtns': totalqtns,
            'qtnlist': qlist,
            'form': form
            })
    #if form is not valid
    else:
      variables = {
                     'examname': ExamName.objects.get(id=request.POST.get("examid", "")).examname,
                     'examid': request.POST.get("examid", ""),
                     'quploaded': ExamQuestions.objects.filter(examname_id=request.POST.get("examid", "")).count(),
                     'form': form
                   }
      #return render(request, 'addquestions.html', variables)
      messages.info(request, 'Error in adding question')
      return HttpResponseRedirect('')

  #if request is not POST
  else:
      return HttpResponseRedirect('')

@login_required
def removequestion_page(request):
  if request.method == 'POST':
    examid = request.POST.get("examid", "")
    qno = request.POST.get("qno", "")
    examquestion = ExamQuestions.objects.filter(examname_id=examid, qno=qno)

    optionA = OptionA.objects.filter(examname_id = examid, qid=qno)
    if optionA.exists():
        optionA.delete()

    optionB = OptionB.objects.filter(examname_id = examid, qid=qno)
    if optionB.exists():
        optionB.delete()

    optionC = OptionC.objects.filter(examname_id = examid, qid=qno)
    if optionC.exists():
        optionC.delete()

    optionD = OptionD.objects.filter(examname_id = examid, qid=qno)
    if optionD.exists():
        optionD.delete()

    optionE = OptionE.objects.filter(examname_id = examid, qid=qno)
    if optionE.exists():
        optionE.delete()

    qinfo = QuestionInfo.objects.filter(examname_id = examid, qid=qno)
    if qinfo.exists():
      if examquestion[0].haspic:
        try:
          os.remove(os.path.join(settings.MEDIA_ROOT, qinfo[0].pic.name))
        except OSError:
          pass
      qinfo.delete()

    solution = ExamSolution.objects.filter(examname_id = examid, qid=qno)
    if solution.exists():
        solution.delete()

    if examquestion.exists():
        examquestion.delete()
    messages.info(request, 'Question deleted successfully.')

    #redirect to question list page
    exam = ExamName.objects.get(id=examid)
    totalqtns = ExamName.objects.get(id=examid).total_questions
    form = QuestionDetailsSaveForm()

    qlist = ExamQuestions.objects.filter(examname_id=examid).order_by('qno')
    return render(request, 'staff/examdetails.html', {
            'examid': examid,
            'examname': exam.examname,
            'totalqtns': totalqtns,
            'qtnlist': qlist,
            'form': form
            })
  #if request is not POST
  else:
      return HttpResponseRedirect('/')

@login_required
def editqtndetail_page(request):
  if request.method == 'POST':
    posted_json = request.POST.get("json", "")
    my_dict = json.loads(posted_json)
    examid = my_dict['examid']
    qno = my_dict['qno']
    resultdict = {}

    examquestion = ExamQuestions.objects.filter(examname_id=examid, qno=qno)

    optionA = OptionA.objects.filter(examname_id = examid, qid=qno)
    if optionA.exists():
      resultdict['optionA'] = optionA[0].option
      resultdict['isOptionA'] = optionA[0].isright
    else:
      resultdict['optionA'] = ""
      resultdict['isOptionA'] = False

    optionB = OptionB.objects.filter(examname_id = examid, qid=qno)
    if optionB.exists():
      resultdict['optionB'] = optionB[0].option
      resultdict['isOptionB'] = optionB[0].isright
    else:
      resultdict['optionB'] = ""
      resultdict['isOptionB'] = False

    optionC = OptionC.objects.filter(examname_id = examid, qid=qno)
    if optionC.exists():
      resultdict['optionC'] = optionC[0].option
      resultdict['isOptionC'] = optionC[0].isright
    else:
      resultdict['optionC'] = ""
      resultdict['isOptionC'] = False

    optionD = OptionD.objects.filter(examname_id = examid, qid=qno)
    if optionD.exists():
      resultdict['optionD'] = optionD[0].option
      resultdict['isOptionD'] = optionD[0].isright
    else:
      resultdict['optionD'] = ""
      resultdict['isOptionD'] = False

    optionE = OptionE.objects.filter(examname_id = examid, qid=qno)
    if optionE.exists():
      resultdict['optionE'] = optionE[0].option
      resultdict['isOptionE'] = optionE[0].isright
    else:
      resultdict['optionE'] = ""
      resultdict['isOptionE'] = False

    qinfo = QuestionInfo.objects.filter(examname_id = examid, qid=qno)
    if qinfo.exists():
        if examquestion[0].haspic:
            try:
                resultdict['picpath'] = qinfo[0].pic.url
            except:
                resultdict['picpath'] = ""
        else:
            resultdict['picpath'] = ""
        resultdict['direction'] = qinfo[0].direction

    resultdict['examid'] = str(examid)
    resultdict['qno'] = str(examquestion[0].qno)
    resultdict['question'] = str(examquestion[0].question)
    resultdict['qtype'] = str(examquestion[0].qtype)
    resultdict['qcategory'] = str(examquestion[0].qcategory)
    resultdict['haspic'] = examquestion[0].haspic
    resultdict['hasdirection'] = examquestion[0].hasdirection
    resultdict['answer'] = str(examquestion[0].answer)

    return HttpResponse(json.dumps(resultdict), content_type="application/json")
  #if request is not POST
  else:
      return HttpResponseRedirect('/')

@login_required
def publishexam_page(request):
  if request.method == 'POST':
    examid = request.POST.get("examid", "")
    cur_val = ExamName.objects.get(id=examid).published
    examname = ExamName.objects.filter(id=examid).update(published= (not cur_val))
    if not cur_val:
       messages.info(request, 'Exam published! Users can now see the exam to add to their account')
    else:
       messages.info(request, 'Exam hidden. Users will not see the exam to add to their account.')
    return HttpResponseRedirect('/')
  else:
    messages.info(request, 'Error in publishing exam!')
    return HttpResponseRedirect('/')

@login_required
def takeexam_page(request):
  if request.method == 'POST':
      #Get userexam
      userexam = UserExams.objects.filter(
        user_id=request.user.id,
        examname_id=request.POST.get("examid", "")
      )
      if userexam.exists():
        totalqtn = ExamQuestions.objects.filter(examname_id=request.POST.get("examid", "")).count()
        examname = ExamName.objects.get(id=request.POST.get("examid", "")).examname

        #allowedAttempt = ExamName.objects.get(id=request.POST.get("examid", "")).attempts_allowed
        allowedAttempt = UserExamAttemptInfo.objects.get(userexam_id=userexam[0].id).attempt_available
        totalqtns = ExamName.objects.get(id=request.POST.get("examid", "")).total_questions
        duration = ExamName.objects.get(id=request.POST.get("examid", "")).duration
        userAttemptCount = UserScoreSheet.objects.filter(
                         user_id=request.user.id,
                         examname_id=request.POST.get("examid", "")
                       ).count()
        if allowedAttempt > userAttemptCount:
          userAttemptCount = userAttemptCount + 1
          scoresheet, created = UserScoreSheet.objects.get_or_create(
                                      user_id=request.user.id, examname_id = request.POST.get("examid", ""), 
                                      attemptid=userAttemptCount, start_time=datetime.now(),
                                      total_questions=totalqtns, answered_questions=0, correctly_answered=0, issubmitted=False, mark=0
                                  )
          variables = RequestContext(request, {
            'examid': request.POST.get("examid", ""),
            'quploaded': range(1, totalqtn + 1),
            'examname': examname,
            'attemptid': userAttemptCount,
            'totalqtns': totalqtn,
            'duration' : duration
          })

          return render(request, 'takeexam.html', {
            'examid': request.POST.get("examid", ""),
            'quploaded': range(1, totalqtn + 1),
            'examname': examname,
            'attemptid': userAttemptCount,
            'totalqtns': totalqtn,
            'duration' : duration
          })

        else:
          messages.info(request, "You ran out of attempts. Please purchase.");
          next = request.POST.get('next', '/')
          return HttpResponseRedirect(next)

  return HttpResponseRedirect('/myaccount')

@login_required
def getqtn_page(request):
  examid = 0
  qno = 0
  variables = RequestContext(request, {})
  optiona = None;
  optionb = None;
  optionc = None;
  optiond = None;
  optione = None;
  if 'examid' in request.GET:
    examid = request.GET['examid'].strip()
  if 'qid' in request.GET:
    qno = request.GET['qid'].strip()
    qdetails = ExamQuestions.objects.filter(examname_id=examid, qno=qno)[0]
    a = OptionA.objects.filter(examname_id=examid, qid=qno)
    b = OptionB.objects.filter(examname_id=examid, qid=qno)
    c = OptionC.objects.filter(examname_id=examid, qid=qno)
    d = OptionD.objects.filter(examname_id=examid, qid=qno)
    e = OptionE.objects.filter(examname_id=examid, qid=qno)

    if a.exists():
      optiona = a[0];
    if b.exists():
      optionb = b[0];
    if c.exists():
      optionc = c[0];
    if d.exists():
      optiond = d[0];
    if e.exists():
      optione = e[0];
    
    variables = RequestContext(request, {
      'qdetails': qdetails,
      'optiona': optiona,
      'optionb': optionb,
      'optionc': optionc,
      'optiond': optiond,
      'optione': optione,
      'examid': examid,
      'qno': qno
    })

  if 'ajax' in request.GET:
    return render(request, 'question.html', {
      'qdetails': qdetails,
      'optiona': optiona,
      'optionb': optionb,
      'optionc': optionc,
      'optiond': optiond,
      'optione': optione,
      'examid': examid,
      'qno': qno
    })

  else:
    return HttpResponseRedirect('/myaccount')

@login_required
@csrf_exempt
def evalexam_page(request):
  if request.method == 'POST':

      posted_json = request.POST.get("json", "")
      my_dict = json.loads(posted_json)
      #Get userexam
      userexam = UserExams.objects.filter(
        user_id=request.user.id,
        examname_id=my_dict["examid"]
      )

      if userexam.exists():
        totalqtns = ExamName.objects.get(id=my_dict["examid"]).total_questions
        rightcount = 0
  
        for key, value in my_dict['ansList'].items():
          solution = ExamSolution.objects.filter(examname_id=my_dict["examid"], qid=key)[0].correct_options

          isRightChoice = False

          if solution.strip() == value.strip():
            isRightChoice = True
            rightcount = rightcount + 1

          useranswer, created = UserAnswerSheet.objects.get_or_create(
              user_id = request.user.id,
              examname_id=my_dict["examid"], attemptid=my_dict["attemptid"], qid=key,
              user_choices=value, user_explanation="", isright = isRightChoice
          )

        scoresheet = UserScoreSheet.objects.get(
                                      user_id=request.user.id, examname_id=my_dict["examid"], 
                                      attemptid=my_dict["attemptid"],
                                      total_questions=totalqtns
                                  )
        scoresheet.answered_questions = len(my_dict['ansList'])
        scoresheet.correctly_answered = rightcount
        scoresheet.issubmitted = True
        scoresheet.mark = rightcount * ExamName.objects.get(id=my_dict["examid"]).mark_per_qtn
        scoresheet.mark = scoresheet.mark - ((len(my_dict['ansList']) - rightcount) * ExamName.objects.get(id=my_dict["examid"]).negative_per_qtn)
        scoresheet.end_time = datetime.now()
        scoresheet.save()

        resultdict = {}
        resultdict['examid'] = scoresheet.examname.id
        resultdict['attemptid'] = scoresheet.attemptid
        resultdict['totalqtns'] = totalqtns
        resultdict['answered_questions'] = len(my_dict['ansList'])
        resultdict['correctly_answered'] = rightcount
        resultdict['mark'] = str(scoresheet.mark)

        msg_html = render_to_string('result_mail.html', {'username': request.user.first_name, 'examid': scoresheet.examname.id, 'attemptid': scoresheet.attemptid, 'examname': scoresheet.examname.examname, 'userscore': scoresheet.mark, 'maxscore': totalqtns * ExamName.objects.get(id=my_dict["examid"]).mark_per_qtn});
        #send_mail(
        #  'QuizBuzz - Result :' + str(scoresheet.examname.examname) + ' - Attempt: ' + str(scoresheet.attemptid),
        #  'Hi ' + str(request.user.first_name) + ',\n\n\
        #   Your score is: ' + str(scoresheet.mark) + '.\n\
        #   Total questions: ' + str(totalqtns) + '.\n\
        #   Answered questions: ' + str(resultdict['answered_questions']) + '.\n\
        #   Correct answers: ' + str(rightcount) + '.\n\nRegards,\nQuizBuzz Team.',
        #  'from@example.com',
        #  [request.user.email],
        #  fail_silently=False,
        #  html_message=msg_html,
        #)
        subject = 'QuizBuzz - Result :' + str(scoresheet.examname.examname) + ' - Attempt: ' + str(scoresheet.attemptid)
        msg = EmailMultiAlternatives(subject, msg_html, "support@quizbuzz.in", [request.user.email], reply_to=["noreply@quizbuzz.in"])
        msg.content_subtype = 'html'  # Main content is text/html  
        msg.mixed_subtype = 'related'  # This is critical, otherwise images will be displayed as attachments!

        for f in ['templates/Images/students.jpg']:
            fp = open(os.path.join(os.path.dirname(__file__), f), 'rb')
            msg_img = MIMEImage(fp.read())
            fp.close()
            msg_img.add_header('Content-ID', '<{}>'.format(f))
            msg.attach(msg_img)
        msg.send()
        return HttpResponse(json.dumps(resultdict))

  return HttpResponseRedirect('/myaccount')

@login_required
@csrf_exempt
def showresult_page(request):
  if request.method == 'POST':
      posted_json = request.POST.get("json", "")
      my_dict = json.loads(posted_json)
      #Get userexam
      userexam = UserExams.objects.filter(
        user_id=request.user.id,
        examname_id=my_dict["examid"]
      )

      if userexam.exists():
        scoresheet = UserScoreSheet.objects.get(
                                      user_id=request.user.id, examname_id=my_dict["examid"], 
                                      attemptid=my_dict["attemptid"]
                                  )
        resultdict = {}
        resultdict['examname'] = str(scoresheet.examname)
        resultdict['attemptid'] = str(scoresheet.attemptid)
        p = re.compile(r'[0-9]+\-[0-9]+\-[0-9]+ [0-9]+\:[0-9]+\:[0-9]+')
        starttime = p.search(str(scoresheet.start_time))
        resultdict['start_time'] = starttime.group()
        endtime = p.search(str(scoresheet.end_time))
        resultdict['end_time'] = endtime.group()
        resultdict['totalqtns'] = str(scoresheet.total_questions)
        resultdict['answered_questions'] = str(scoresheet.answered_questions)
        resultdict['correctly_answered'] = str(scoresheet.correctly_answered)
        resultdict['mark'] = str(scoresheet.mark)
        return HttpResponse(json.dumps(resultdict))

  return HttpResponseRedirect('/myaccount')

@login_required
def get_graph_data(request):
  examid = 0
  
  JSONObj = {
  };

  if 'examid' in request.GET:
    examid = request.GET['examid'].strip()



    userscoresheet = UserScoreSheet.objects.filter(
                         user_id=request.user.id,
                         examname_id=request.GET.get('examid', "0"),
                         attemptid=request.GET.get('attemptid', "0")
                       )

    if userscoresheet.exists():
       JSONObj['unanswered'] = (userscoresheet[0].total_questions - userscoresheet[0].answered_questions);
       JSONObj['correctanswers'] = (userscoresheet[0].correctly_answered);
       JSONObj['wronganswers'] = (userscoresheet[0].answered_questions - userscoresheet[0].correctly_answered);
       return HttpResponse(json.dumps(JSONObj), content_type="application/json")

  return HttpResponse(json.dumps(JSONObj), content_type="application/json")

@login_required
def get_profile_data(request):
  JSONObj = {
    "uname" : request.user.username
  };

  user = User.objects.get(username=request.user.username)
  if request.method == 'GET':
    JSONObj['firstname'] = user.first_name;
    JSONObj['lastname'] = user.last_name;
    JSONObj['email'] = user.email;
    
    userdetail = UserDetails.objects.filter(user_id=request.user.id)

    if userdetail.exists():
      JSONObj['address'] = str(userdetail[0].address)
      JSONObj['city'] = str(userdetail[0].city)
      JSONObj['country'] = str(userdetail[0].country)
      JSONObj['pincode'] = str(userdetail[0].pincode)
      JSONObj['aboutme'] = str(userdetail[0].aboutme)
    else:
      JSONObj['address'] = ""
      JSONObj['city'] = ""
      JSONObj['country'] = ""
      JSONObj['pincode'] = ""
      JSONObj['aboutme'] = ""

    return HttpResponse(json.dumps(JSONObj), content_type="application/json")
  else:
    return HttpResponse(json.dumps(JSONObj), content_type="application/json")

@login_required
def fetchQuestionPaperJSON(request):
  examid = 0
  
  if 'examid' in request.GET:
    examid = request.GET['examid'].strip()

    JSONObj = {
      "qlist" : []
    };

    qlist = ExamQuestions.objects.filter(examname_id=examid).order_by('qno')

    for qtn in qlist:
        qdict = {}
        qdict['qno'] = qtn.qno
        qdict['qtn'] = qtn.question
        qdict['type'] = qtn.qtype
        qdict['qcategory'] = qtn.qcategory
        qdict['options'] = [];
        qdict['haspic'] = qtn.haspic;
        qdict['hasdirection'] = qtn.hasdirection;

        if qtn.haspic or qtn.hasdirection:
            qinfo = QuestionInfo.objects.filter(examname_id=examid, qid=qtn.qno)

            if qinfo.exists() and qtn.haspic:
                qdict['imgpath'] = qinfo[0].pic.url;

            if qinfo.exists() and qtn.hasdirection:
                qdict['direction'] = qinfo[0].direction;

        a = OptionA.objects.filter(examname_id=examid, qid=qtn.qno)
        b = OptionB.objects.filter(examname_id=examid, qid=qtn.qno)
        c = OptionC.objects.filter(examname_id=examid, qid=qtn.qno)
        d = OptionD.objects.filter(examname_id=examid, qid=qtn.qno)
        e = OptionE.objects.filter(examname_id=examid, qid=qtn.qno)

        if a.exists():
          opta = {}
          opta['option'] = a[0].option;
          opta['checked'] = "false";
          qdict['options'].append(opta);
        if b.exists():
          optb = {}
          optb['option'] = b[0].option;
          optb['checked'] = "false";
          qdict['options'].append(optb);
        if c.exists():
          optc = {}
          optc['option'] = c[0].option;
          optc['checked'] = "false";
          qdict['options'].append(optc);
        if d.exists():
          optd = {}
          optd['option'] = d[0].option;
          optd['checked'] = "false";
          qdict['options'].append(optd);
        JSONObj['qlist'].append(qdict)


  if 'ajax' in request.GET:
    return HttpResponse(json.dumps(JSONObj), content_type="application/json")

@login_required
def history_page(request):

  current_page = int(request.GET.get('page' ,1))
  limit = 10 * current_page
  offset = limit - 10

  historylist = UserScoreSheet.objects.filter(user_id=request.user.id, issubmitted=True).order_by('-end_time')[offset:limit]

  total_list = UserScoreSheet.objects.filter(user_id=request.user.id, issubmitted=True).count()

  total_pages = int(total_list / 10)

  reminder = total_list % 10

  if reminder:
     total_pages += 1 # adding one more page if the last page will contains less contacts 

  pagination = make_pagination_html(current_page, total_pages)

  variables = RequestContext(request, {
    'historylist': historylist
  })
  return render(request, 'history_page.html', {
    'historylist': historylist,
    'pagination': pagination,
    'offset': offset
  })

def make_pagination_html(current_page, total_pages):

    pagination_string = ""

    if current_page > 1:
        pagination_string += '<a href="?page=%s">previous</a>' % (current_page -1)

    pagination_string += '<span class="current"> Page %s of %s </span>' %(current_page, total_pages)

    if current_page < total_pages:
        pagination_string += '<a href="?page=%s">next</a>' % (current_page + 1)

    return pagination_string

@login_required
def analysis_page(request):

  current_page = int(request.GET.get('page' ,1))
  limit = 10 * current_page
  offset = limit - 10

  analyticslist = UserScoreSheet.objects.filter(user_id=request.user.id, issubmitted=True).order_by('-end_time')[offset:limit]

  total_list = UserScoreSheet.objects.filter(user_id=request.user.id, issubmitted=True).count()

  total_pages = int(total_list / 10)

  reminder = total_list % 10

  if reminder:
     total_pages += 1 # adding one more page if the last page will contains less contacts 

  pagination = make_pagination_html(current_page, total_pages)
  variables = RequestContext(request, {
    'analyticslist': analyticslist
  })
  return render(request, 'analytics_page.html', {
    'analyticslist': analyticslist,
    'pagination': pagination
  })

@login_required
def review_page(request):
  if request.method == 'POST':
      #Get userexam
      userexam = UserExams.objects.filter(
        user_id=request.user.id,
        examname_id=request.POST.get('examid', "")
      )
      if userexam.exists():
        totalqtn = ExamQuestions.objects.filter(examname_id=request.POST.get('examid', "")).count()
        examname = ExamName.objects.get(id=request.POST.get('examid', "")).examname

        totalqtns = ExamName.objects.get(id=request.POST.get('examid', "")).total_questions
        userAttemptCount = UserScoreSheet.objects.filter(
                         user_id=request.user.id,
                         examname_id=request.POST.get('examid', "")
                       ).count()
        variables = RequestContext(request, {
          'examid': request.POST.get('examid', ""),
          'quploaded': range(1, totalqtn + 1),
          'examname': examname,
          'attemptid': request.POST.get('attemptid', ""),
          'totalqtns': totalqtn
        })

        return render(request, 'reviewexam.html', {
          'examid': request.POST.get('examid', ""),
          'quploaded': range(1, totalqtn + 1),
          'examname': examname,
          'attemptid': request.POST.get('attemptid', ""),
          'totalqtns': totalqtn
        })

      else:
        return HttpResponseRedirect('/')

  return HttpResponseRedirect('/')

@login_required
def examdetails_page(request):
    if request.method == 'POST':
        exam = ExamName.objects.get(id=request.POST.get('examid', ""))
        totalqtns = ExamName.objects.get(id=request.POST.get('examid', "")).total_questions

        qlist = ExamQuestions.objects.filter(examname_id=request.POST.get('examid', "")).order_by('qno')
        form = QuestionDetailsSaveForm()
        return render(request, 'staff/examdetails.html', {
            'examid': request.POST.get('examid', ""),
            'examname': exam.examname,
            'totalqtns': totalqtns,
            'qtnlist': qlist,
            'form': form
            })
    else:
        messages.info(request, 'Invalid Exam!')
        return HttpResponseRedirect('/')


@login_required
def analyzegraphs_page(request):
  if request.method == 'POST':
      #Get userexam
      userexam = UserExams.objects.filter(
        user_id=request.user.id,
        examname_id=request.POST.get('examid', "")
      )
      if userexam.exists():
        totalqtn = ExamQuestions.objects.filter(examname_id=request.POST.get('examid', "")).count()
        examname = ExamName.objects.get(id=request.POST.get('examid', "")).examname

        totalqtns = ExamName.objects.get(id=request.POST.get('examid', "")).total_questions

        userscoresheet = UserScoreSheet.objects.filter(
                         user_id=request.user.id,
                         examname_id=request.POST.get('examid', "0"),
                         attemptid=request.POST.get('attemptid', "0")
                       )

        totalanswered = userscoresheet[0].answered_questions;
        correctans = userscoresheet[0].correctly_answered;
        markscored = userscoresheet[0].mark;
        timediff = userscoresheet[0].end_time - userscoresheet[0].start_time
        p = re.compile(r'[0-9]+\:[0-9]+\:[0-9]+');
        duration = p.search(str(timediff));
        timetaken= duration.group();
        totalmarks = ExamName.objects.get(id=request.POST.get('examid', "")).total_questions * ExamName.objects.get(id=request.POST.get('examid', "")).mark_per_qtn
        variables = RequestContext(request, {
          'examid': request.POST.get('examid', ""),
          'quploaded': range(1, totalqtn + 1),
          'examname': examname,
          'attemptid': request.POST.get('attemptid', ""),
          'totalqtns': totalqtn
        })

        return render(request, 'analyzeexam.html', {
          'examid': request.POST.get('examid', ""),
          'quploaded': range(1, totalqtn + 1),
          'examname': examname,
          'attemptid': request.POST.get('attemptid', ""),
          'totalqtns': totalqtn,
          'totalmarks': totalmarks,
          'totalanswered': totalanswered,
          'markscored': markscored,
          'timetaken': timetaken,
          'correctans': correctans
        })

      else:
        return HttpResponseRedirect('/')

  return HttpResponseRedirect('/')

@login_required
def fetchSolutionJSON(request):
  examid = 0
  
  if 'examid' in request.GET:
    examid = request.GET['examid'].strip()

    JSONObj = {
      "qlist" : []
    };

    qlist = ExamQuestions.objects.filter(examname_id=examid).order_by('qno')

    for qtn in qlist:
        solutionObject = ExamSolution.objects.filter(examname_id=examid, qid=qtn.qno)
        userAnswerObject = UserAnswerSheet.objects.filter(user_id=request.user.id, examname_id=examid, attemptid=request.GET['attemptid'].strip(), qid=qtn.qno)
        explanation = ""
        if solutionObject.exists():
          explanation = solutionObject[0].explanation
        qdict = {}
        qdict['qno'] = qtn.qno
        qdict['qtn'] = qtn.question
        qdict['type'] = qtn.qtype
        qdict['qcategory'] = qtn.qcategory
        qdict['options'] = [];
        qdict['explanation'] = explanation;

        qdict['haspic'] = qtn.haspic;
        qdict['hasdirection'] = qtn.hasdirection;

        if qtn.haspic or qtn.hasdirection:
            qinfo = QuestionInfo.objects.filter(examname_id=examid, qid=qtn.qno)

            if qinfo.exists() and qtn.haspic:
                qdict['imgpath'] = qinfo[0].pic.url;

            if qinfo.exists() and qtn.hasdirection:
                qdict['direction'] = qinfo[0].direction;

        a = OptionA.objects.filter(examname_id=examid, qid=qtn.qno)
        b = OptionB.objects.filter(examname_id=examid, qid=qtn.qno)
        c = OptionC.objects.filter(examname_id=examid, qid=qtn.qno)
        d = OptionD.objects.filter(examname_id=examid, qid=qtn.qno)
        e = OptionE.objects.filter(examname_id=examid, qid=qtn.qno)

        if a.exists():
          opta = {}
          opta['option'] = a[0].option;
          if userAnswerObject.exists():
            if "1" in str(userAnswerObject[0].user_choices):
              opta['checked'] = "true";
            else:
              opta['checked'] = "false";
          else:
            opta['checked'] = "false";
          opta['isright'] = a[0].isright;
          qdict['options'].append(opta);
        if b.exists():
          optb = {}
          optb['option'] = b[0].option;
          if userAnswerObject.exists():
            if "2" in str(userAnswerObject[0].user_choices):
              optb['checked'] = "true";
            else:
              optb['checked'] = "false";
          else:
            optb['checked'] = "false";
          optb['isright'] = b[0].isright;
          qdict['options'].append(optb);
        if c.exists():
          optc = {}
          optc['option'] = c[0].option;
          if userAnswerObject.exists():
            if "3" in str(userAnswerObject[0].user_choices):
              optc['checked'] = "true";
            else:
              optc['checked'] = "false";
          else:
            optc['checked'] = "false";
          optc['isright'] = c[0].isright;
          qdict['options'].append(optc);
        if d.exists():
          optd = {}
          optd['option'] = d[0].option;
          if userAnswerObject.exists():
            if "4" in str(userAnswerObject[0].user_choices):
              optd['checked'] = "true";
            else:
              optd['checked'] = "false";
          else:
            optd['checked'] = "false";
          optd['isright'] = d[0].isright;
          qdict['options'].append(optd);
        JSONObj['qlist'].append(qdict)


  if 'ajax' in request.GET:
    return HttpResponse(json.dumps(JSONObj), content_type="application/json")

#For reset password
class ResetPasswordRequestView(FormView):
    template_name = "account/test_template.html"    #code for template is given below the view's code
    success_url = '/reset_password'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        """
        This method here validates the if the input is an email address or not. Its return type is boolean, True if the input is a email address or False if its not.
        """
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        '''
        A normal post request which takes input from field "email_or_username" (in ResetPasswordRequestForm). 
        '''
        form = self.form_class(request.POST)
        if form.is_valid():
            data= form.cleaned_data["email_or_username"]
        if self.validate_email_address(data) is True:                 #uses the method written above
            '''
            If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.
            '''
            associated_users= User.objects.filter(Q(email=data)|Q(username=data))
            if associated_users.exists():
                for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'QuizBuzz.in',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            }
                        subject_template_name='registration/password_reset_subject.txt' 
                        # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                        email_template_name='registration/password_reset_email.html'    
                        # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                        subject = loader.render_to_string(subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, 'from@example.com', [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'No user is associated with this email address')
            return result
        else:
            '''
            If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
            '''
            associated_users= User.objects.filter(username=data)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': 'quizbuzz.in', #or your domain eg:example.com
                        'site_name': 'QuizBuzz',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                    subject_template_name='registration/password_reset_subject.txt'
                    email_template_name='registration/password_reset_email.html'
                    subject = loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, 'from@example.com' , [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'Email has been sent to the email address associated with the username \'' + data +"\'. Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'This username does not exist in the system.')
            return result
        messages.error(request, 'Invalid Input')
        return self.form_invalid(form)

class PasswordResetConfirmView(FormView):
    template_name = "account/test_template.html"
    success_url = '/login/'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password= form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password reset successfully. Login with your new password.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset failed.')
                return self.form_invalid(form)
        else:
            messages.error(request,'The reset password link is no longer valid.')
            return self.form_invalid(form)

'''
===Payment ===
'''

def payment(request):   
    data = {}

    examid = request.POST.get("examid", 0)
    exam_price = ExamName.objects.get(id=request.POST.get("examid", "")).price
    examname = ExamName.objects.get(id=request.POST.get("examid", "")).examname
    txnid = get_transaction_id()
    hash_ = generate_hash(request, txnid, examid, exam_price, examname)
    hash_string = get_hash_string(request, txnid, examid, exam_price, examname)
    # use constants file to store constant values.
    # use test URL for testing
    data["action"] = constants.PAYMENT_URL_TEST 
    data["amount"] = float(exam_price)
    data["productinfo"]  = examname
    data["key"] = config.KEY
    data["txnid"] = txnid
    data["hash"] = hash_
    data["hash_string"] = hash_string
    data["firstname"] = request.user.username
    data["email"] = request.user.email
    data["phone"] = "9123456780"
    data["service_provider"] = constants.SERVICE_PROVIDER
    data["udf1"] = examid
    data["furl"] = request.build_absolute_uri(reverse("payment_failure"))
    data["surl"] = request.build_absolute_uri(reverse("payment_success"))
    
    return render(request, "payment/payment_form.html", data)        
    
# generate the hash
def generate_hash(request, txnid, examid, exam_price, examname):
    try:
        # get keys and SALT from dashboard once account is created.
        # hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        hash_string = get_hash_string(request,txnid, examid, exam_price, examname)
        generated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
        return generated_hash
    except Exception as e:
        # log the error here.
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None
 
# create hash string using all the fields
def get_hash_string(request, txnid, examid, exam_price, examname):
    hash_string = config.KEY+"|"+txnid+"|"+str(float(exam_price))+"|"+examname+"|"
    hash_string += request.user.username+"|"+request.user.email+"|"
    hash_string += examid + "||||||||||"+config.SALT
 
    return hash_string
 
# generate a random transaction Id.
def get_transaction_id():
    hash_object = hashlib.sha256(str(randint(0,9999)).encode("utf-8"))
    # take approprite length
    txnid = hash_object.hexdigest().lower()[0:32]
    return txnid
 
# no csrf token require to go to Success page. 
# This page displays the success/confirmation message to user indicating the completion of transaction.
@csrf_exempt
def payment_success(request):
    data = {}
    examname_id=request.POST.get("udf1", "")
    data['examid'] = examname_id

    data['amount'] = request.POST.get("amount", "")
    data['txnid'] = request.POST.get("txnid", "")
    data['productinfo'] = request.POST.get("productinfo", "")
    data['email'] = request.POST.get("email", "")
    data['firstname'] = request.POST.get("firstname", "")
    data['examname'] = ExamName.objects.get(id=examname_id).examname

    #send mail
    msg_html = render_to_string('payment/paysuccess_mail.html', data);
    subject = 'QuizBuzz - Order Confirmation'
    msg = EmailMultiAlternatives(subject, msg_html, "support@quizbuzz.in", [request.user.email], reply_to=["noreply@quizbuzz.in"])
    msg.content_subtype = 'html'  # Main content is text/html  
    msg.mixed_subtype = 'related'  # This is critical, otherwise images will be displayed as attachments!
    msg.send()


    userexam, created = UserExams.objects.get_or_create(
        user_id=request.user.id,
        examname_id=data['examid']
    )

    attempts_per_purchase = ExamName.objects.get(id=examname_id).attempts_allowed

    if created:
        #create userexamattemptinfo with attempts per purchase from examname
        uexam_attempt, dummy = UserExamAttemptInfo.objects.get_or_create(
                userexam_id = userexam.id,
                attempt_available = attempts_per_purchase
            )
    else:
        #update userexamattemptinfo with additional attempts per purchase from examname
        uexamattemptinfo = UserExamAttemptInfo.objects.get(userexam_id=userexam.id)
        current_available_attempts = uexamattemptinfo.attempt_available
        new_attempts = attempts_per_purchase + current_available_attempts
        uexamattemptinfo.attempt_available = new_attempts
        uexamattemptinfo.save()

    messages.info(request, "Payment Successful! Exam added to your account.")
    return render(request, "payment/success.html", data)
 
# no csrf token require to go to Failure page. This page displays the message and reason of failure.
@csrf_exempt
def payment_failure(request):
    data = {}
    examname_id=request.POST.get("udf1", "")
    data['examid'] = examname_id
    data['amount'] = request.POST.get("amount", "")
    data['txnid'] = request.POST.get("txnid", "")
    data['productinfo'] = request.POST.get("productinfo", "")
    data['email'] = request.POST.get("email", "")
    data['firstname'] = request.POST.get("firstname", "")
    data['examname'] = ExamName.objects.get(id=examname_id).examname

    #send mail
    msg_html = render_to_string('payment/payfail_mail.html', data);
    subject = 'QuizBuzz - Order Status'
    msg = EmailMultiAlternatives(subject, msg_html, "support@quizbuzz.in", [request.user.email], reply_to=["noreply@quizbuzz.in"])
    msg.content_subtype = 'html'  # Main content is text/html  
    msg.mixed_subtype = 'related'  # This is critical, otherwise images will be displayed as attachments!
    msg.send()


    messages.info(request, "Payment Failed! Please try again.")
    return render(request, "payment/failure.html", data)


'''
===Payment End===
'''
'''
    JSONObjSample = {
      "qlist" : [
         {
           "qno" : "1",
           "qtn" : "What is your name?",
           "qcategory" : "1",
           "type" : "1",
           "options" : [
              {"option" : "Vinoth", "checked" : "false"},
              {"option" : "Kumar", "checked" : "false"},
              {"option" : "Sachin", "checked" : "false"},
              {"option" : "Dravid", "checked" : "false"}
           ]
         },
         {
           "qno" : "2",
           "qtn" : "What is your company's name?",
           "qcategory" : "1",
           "type" : "1",
           "options" : [
              {"option" : "Aricent", "checked" : "false"},
              {"option" : "Cavium", "checked" : "false"},
              {"option" : "Samsung", "checked" : "false"},
              {"option" : "Mentor Graphics", "checked" : "false"}
           ]
         },
         {
           "qno" : "3",
           "qtn" : "What is your qualification?",
           "qcategory" : "2",
           "type" : "1",
           "options" : [
              {"option" : "10", "checked" : "false"},
              {"option" : "10 + 2", "checked" : "false"},
              {"option" : "Under Graduate", "checked" : "false"},
              {"option" : "Post Graduate", "checked" : "false"}
           ]
         },
         {
           "qno" : "4",
           "qtn" : "Who is your favourite player?",
           "qcategory" : "2",
           "type" : "2",
           "options" : [
              {"option" : "Ganguly", "checked" : "false"},
              {"option" : "Dhoni", "checked" : "false"},
              {"option" : "Sachin", "checked" : "false"},
              {"option" : "Dravid", "checked" : "false"}
           ]
         }
       ]
    };
'''
