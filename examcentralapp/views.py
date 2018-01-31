from django.shortcuts import render
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

#For Reset password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
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

def main_page(request):
  
  examlist = ExamName.objects.filter(published=True)
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
    return render(request, 'main_page.html', { 'form': form,
    'examlist': examlist,
    'show_results': show_results,
    'show_tags': True
    })


def user_loggedin(request):
  if request.user.is_authenticated():
    username = request.user.username
  redirect_url = '/user/' + username
  return HttpResponseRedirect(redirect_url)

@login_required
def user_page(request, username):
  user = get_object_or_404(User, username=username)
  exams = user.userexams_set.order_by('-id')

  variables = RequestContext(request, {
    'username': username,
    'userexams': exams,
    'show_tags': True
  })
  return render(request, 'user_page.html', {
    'username': username,
    'userexams': exams,
    'show_tags': True
  })


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
      send_mail(
        'ExamCentral - Account Registration',
        'Hi,\n\n\
         Your Email Id is registered with ExamCentral.com.\n\
         Your Username: ' + form.cleaned_data['username'] + '\n\nThanks,\nExamCentral Team.',
        'from@example.com',
        [form.cleaned_data['email']],
        fail_silently=False,
      )
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

@login_required
def examdetails_save_page(request):
  if request.method == 'POST':
    form = ExamDetailsSaveForm(request.POST)
    if form.is_valid():
      # Create or get Exam Detail.
      examname, created = ExamName.objects.get_or_create(
        examname=form.cleaned_data['examname'], total_questions=form.cleaned_data['total_questions'],
        attempts_allowed=form.cleaned_data['attempts_allowed'], duration=form.cleaned_data['duration'],
        start_time=form.cleaned_data['start_time'], end_time=form.cleaned_data['end_time'], price=form.cleaned_data['price'],
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

      return render(request, 'addquestions.html', {
                     'examname': examname.examname,
                     'examid': examname.id,
                     'quploaded': 0,
                     'form': form
                   })

  else:
    form = ExamDetailsSaveForm()
  variables = RequestContext(request, {
    'form': form
  })
  return render(request, 'examdetail_save.html',  {
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
      userexam, dummy = UserExams.objects.get_or_create(
        user_id=request.user.id,
        examname_id=request.POST.get("examid", "")
      )
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
    form = QuestionDetailsSaveForm(request.POST)
    if form.is_valid():
      right_options = ""
      # Add question
      examquestion, created = ExamQuestions.objects.get_or_create(
        examname_id=request.POST.get("examid", ""), qno=form.cleaned_data['qno'], question=form.cleaned_data['question'],
        qtype=form.cleaned_data['qtype'], qcategory=form.cleaned_data['qcategory'],
        answer=form.cleaned_data['answer']
      )

      isOptionA = request.POST.get('isOptionA', 0)
      optionA, created = OptionA.objects.get_or_create(
        examname_id = request.POST.get("examid", ""), qid=form.cleaned_data['qno'], option=form.cleaned_data['optionA'],
        isright = isOptionA
      )

      isOptionB = request.POST.get('isOptionB', 0)
      optionB, created = OptionB.objects.get_or_create(
        examname_id = request.POST.get("examid", ""), qid=form.cleaned_data['qno'], option=form.cleaned_data['optionB'],
        isright = isOptionB
      )

      isOptionC = request.POST.get('isOptionC', 0)
      if request.POST.get("optionC", ""):
        optionC, created = OptionC.objects.get_or_create(
          examname_id = request.POST.get("examid", ""), qid=form.cleaned_data['qno'], option=form.cleaned_data['optionC'],
          isright = isOptionC
        )

      isOptionD = request.POST.get('isOptionD', 0)
      if request.POST.get("optionD", ""):
        optionD, created = OptionD.objects.get_or_create(
          examname_id = request.POST.get("examid", ""), qid=form.cleaned_data['qno'], option=form.cleaned_data['optionD'],
          isright = isOptionD
        )

      if isOptionA:
        right_options += "1"
      if isOptionB:
        right_options += " 2"
      if isOptionC:
        right_options += " 3"
      if isOptionD:
        right_options += " 4"

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

      return render(request, 'addquestions.html', variables)
    #if form is not valid
    else:
      variables = {
                     'examname': ExamName.objects.get(id=request.POST.get("examid", "")).examname,
                     'examid': request.POST.get("examid", ""),
                     'quploaded': ExamQuestions.objects.filter(examname_id=request.POST.get("examid", "")).count(),
                     'form': form
                   }
      return render(request, 'addquestions.html', variables)

  #if request is not POST
  else:
    form = QuestionDetailsSaveForm()

  variables = {
                 'examname': examname.examname,
                 'examid': examname.id,
                 'quploaded': 0,
                 'form': form
              }
  return render(request, 'addquestions.html', variables)

@login_required
def publishexam_page(request):
  if request.method == 'POST':
    examid = request.POST.get("examid", "")
    examname = ExamName.objects.filter(id=examid).update(published=1)
    return HttpResponseRedirect('/')
  else:
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

        allowedAttempt = ExamName.objects.get(id=request.POST.get("examid", "")).attempts_allowed
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
          return HttpResponseRedirect('/myaccount')

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
  if 'examid' in request.GET:
    examid = request.GET['examid'].strip()
  if 'qid' in request.GET:
    qno = request.GET['qid'].strip()
    qdetails = ExamQuestions.objects.filter(examname_id=examid, qno=qno)[0]
    a = OptionA.objects.filter(examname_id=examid, qid=qno)
    b = OptionB.objects.filter(examname_id=examid, qid=qno)
    c = OptionC.objects.filter(examname_id=examid, qid=qno)
    d = OptionD.objects.filter(examname_id=examid, qid=qno)

    if a.exists():
      optiona = a[0];
    if b.exists():
      optionb = b[0];
    if c.exists():
      optionc = c[0];
    if d.exists():
      optiond = d[0];
    
    variables = RequestContext(request, {
      'qdetails': qdetails,
      'optiona': optiona,
      'optionb': optionb,
      'optionc': optionc,
      'optiond': optiond,
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
        send_mail(
          'ExamCentral - Result :' + str(scoresheet.examname.examname) + ' - Attempt: ' + str(scoresheet.attemptid),
          'Hi ' + str(request.user.first_name) + ',\n\n\
           Your score is: ' + str(scoresheet.mark) + '.\n\
           Total questions: ' + str(totalqtns) + '.\n\
           Answered questions: ' + str(resultdict['answered_questions']) + '.\n\
           Correct answers: ' + str(rightcount) + '.\n\nRegards,\nExamCentral Team.',
          'from@example.com',
          [request.user.email],
          fail_silently=False,
          html_message=msg_html,
        )
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
        resultdict['start_time'] = str(scoresheet.start_time)
        resultdict['end_time'] = str(scoresheet.end_time)
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
        a = OptionA.objects.filter(examname_id=examid, qid=qtn.qno)
        b = OptionB.objects.filter(examname_id=examid, qid=qtn.qno)
        c = OptionC.objects.filter(examname_id=examid, qid=qtn.qno)
        d = OptionD.objects.filter(examname_id=examid, qid=qtn.qno)

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
  historylist = UserScoreSheet.objects.filter(user_id=request.user.id, issubmitted=True)

  variables = RequestContext(request, {
    'historylist': historylist
  })
  return render(request, 'history_page.html', {
    'historylist': historylist
  })

@login_required
def analysis_page(request):
  analyticslist = UserScoreSheet.objects.filter(user_id=request.user.id, issubmitted=True)

  variables = RequestContext(request, {
    'analyticslist': analyticslist
  })
  return render(request, 'analytics_page.html', {
    'analyticslist': analyticslist
  })

@login_required
def review_page(request):
  if request.method == 'GET':
      #Get userexam
      userexam = UserExams.objects.filter(
        user_id=request.user.id,
        examname_id=request.GET.get('examid', "")
      )
      if userexam.exists():
        totalqtn = ExamQuestions.objects.filter(examname_id=request.GET.get('examid', "")).count()
        examname = ExamName.objects.get(id=request.GET.get('examid', "")).examname

        totalqtns = ExamName.objects.get(id=request.GET.get('examid', "")).total_questions
        userAttemptCount = UserScoreSheet.objects.filter(
                         user_id=request.user.id,
                         examname_id=request.GET.get('examid', "")
                       ).count()
        variables = RequestContext(request, {
          'examid': request.GET.get('examid', ""),
          'quploaded': range(1, totalqtn + 1),
          'examname': examname,
          'attemptid': request.GET.get('attemptid', ""),
          'totalqtns': totalqtn
        })

        return render(request, 'reviewexam.html', {
          'examid': request.GET.get('examid', ""),
          'quploaded': range(1, totalqtn + 1),
          'examname': examname,
          'attemptid': request.GET.get('attemptid', ""),
          'totalqtns': totalqtn
        })

      else:
        return HttpResponseRedirect('/')

  return HttpResponseRedirect('/')

@login_required
def analyzegraphs_page(request):
  if request.method == 'GET':
      #Get userexam
      userexam = UserExams.objects.filter(
        user_id=request.user.id,
        examname_id=request.GET.get('examid', "")
      )
      if userexam.exists():
        totalqtn = ExamQuestions.objects.filter(examname_id=request.GET.get('examid', "")).count()
        examname = ExamName.objects.get(id=request.GET.get('examid', "")).examname

        totalqtns = ExamName.objects.get(id=request.GET.get('examid', "")).total_questions
        userAttemptCount = UserScoreSheet.objects.filter(
                         user_id=request.user.id,
                         examname_id=request.GET.get('examid', "")
                       ).count()
        variables = RequestContext(request, {
          'examid': request.GET.get('examid', ""),
          'quploaded': range(1, totalqtn + 1),
          'examname': examname,
          'attemptid': request.GET.get('attemptid', ""),
          'totalqtns': totalqtn
        })

        return render(request, 'analyzeexam.html', {
          'examid': request.GET.get('examid', ""),
          'quploaded': range(1, totalqtn + 1),
          'examname': examname,
          'attemptid': request.GET.get('attemptid', ""),
          'totalqtns': totalqtn
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
        a = OptionA.objects.filter(examname_id=examid, qid=qtn.qno)
        b = OptionB.objects.filter(examname_id=examid, qid=qtn.qno)
        c = OptionC.objects.filter(examname_id=examid, qid=qtn.qno)
        d = OptionD.objects.filter(examname_id=examid, qid=qtn.qno)

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
                            'site_name': 'your site',
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
                        'domain': 'kumarinba.pythonanywhere.com', #or your domain eg:example.com
                        'site_name': 'ExamCentral',
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
                messages.success(request, 'Email has been sent to ' + data +"'s email address. Please check its inbox to continue reseting password.")
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
                messages.success(request, 'Password has been reset. Login with your new password.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset has not been successful.')
                return self.form_invalid(form)
        else:
            messages.error(request,'The reset password link is no longer valid.')
            return self.form_invalid(form)

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
