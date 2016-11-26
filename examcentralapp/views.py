from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

# Create your views here.
from django.http import HttpResponse, Http404
from django.template import Context
from django.template.loader import get_template
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

def main_page(request):
  
  examlist = ExamName.objects.filter(published=True)
  #variables = RequestContext(request, {'examlist': examlist})
  #return render_to_response(
  #  'main_page.html', variables
  #)
  form = SearchForm()
  
  show_results = True
  if request.GET.has_key('query'):
    show_results = True
    query = request.GET['query'].strip()
    if query:
      form = SearchForm({'query' : query}) 
      examlist = ExamName.objects.filter(examname__icontains=query)[:10]
    if request.GET.has_key('blank'):
      examlist = ExamName.objects.filter(published=True)
  variables = RequestContext(request, { 'form': form,
    'examlist': examlist,
    'show_results': show_results,
    'show_tags': True
  })

  if request.GET.has_key('ajax'):
    return render_to_response('examlist.html', variables)
  else:
    return render_to_response('main_page.html', variables)

def user_loggedin(request):
  if request.user.is_authenticated():
    username = request.user.username
  redirect_url = '/user/' + username
  return HttpResponseRedirect(redirect_url)

def user_page(request, username):
  user = get_object_or_404(User, username=username)
  exams = user.userexams_set.order_by('-id')

  variables = RequestContext(request, {
    'username': username,
    'userexams': exams,
    'show_tags': True
  })
  return render_to_response('user_page.html', variables)

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

  return render_to_response(
    'registration/register.html', 
    variables
  )

@login_required
def examdetails_save_page(request):
  if request.method == 'POST':
    form = ExamDetailsSaveForm(request.POST)
    if form.is_valid():
      # Create or get Exam Detail.
      examname, created = ExamName.objects.get_or_create(
        examname=form.cleaned_data['examname'], total_questions=form.cleaned_data['total_questions'],
        attempts_allowed=form.cleaned_data['attempts_allowed'],
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

      return render_to_response('addquestions.html', variables)

  else:
    form = ExamDetailsSaveForm()
  variables = RequestContext(request, {
    'form': form
  })
  return render_to_response('examdetail_save.html', variables)

def search_page(request):
  form = SearchForm()
  examlist = []
  show_results = False
  if request.GET.has_key('query'):
    show_results = True
    query = request.GET['query'].strip()
    if query:
      form = SearchForm({'query' : query}) 
      examlist = ExamName.objects.filter(examname__icontains=query)[:10]
  if request.GET.has_key('blank'):
    examlist = ExamName.objects.filter(published=True)
  variables = RequestContext(request, { 'form': form,
    'form': form,
    'examlist': examlist,
    'show_results': show_results,
    'show_tags': True,
    'show_user': True
  })

  if request.GET.has_key('ajax'):
    return render_to_response('examlist.html', variables)
  else:
    return render_to_response('search.html', variables)


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
      variables =  RequestContext(request, {
                     'examname': examname,
                     'examid': request.POST.get("examid", ""),
                     'quploaded': uploaded_questions,
                     'form': form
                   })

      return render_to_response('addquestions.html', variables)
    #if form is not valid
    else:
      variables = RequestContext(request, {
                     'examname': ExamName.objects.get(id=request.POST.get("examid", "")).examname,
                     'examid': request.POST.get("examid", ""),
                     'quploaded': ExamQuestions.objects.filter(examname_id=request.POST.get("examid", "")).count(),
                     'form': form
                   })
      return render_to_response('addquestions.html', variables)

  #if request is not POST
  else:
    form = QuestionDetailsSaveForm()

  variables =  RequestContext(request, {
                 'examname': examname.examname,
                 'examid': examname.id,
                 'quploaded': 0,
                 'form': form
               })
  return render_to_response('addquestions.html', variables)

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
            'totalqtns': totalqtn
          })

          return render_to_response('takeexam.html', variables)

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
  if request.GET.has_key('examid'):
    examid = request.GET['examid'].strip()
  if request.GET.has_key('qid'):
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

  if request.GET.has_key('ajax'):
    return render_to_response('question.html', variables)
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
        scoresheet.mark = rightcount * 1
        scoresheet.end_time = datetime.now()
        scoresheet.save()

        resultdict = {}
        resultdict['totalqtns'] = totalqtns
        resultdict['answered_questions'] = len(my_dict['ansList'])
        resultdict['correctly_answered'] = rightcount
        resultdict['mark'] = rightcount * 1

        return HttpResponse(json.dumps(resultdict))
        #return render_to_response('showresult.html', variables)

  #return HttpResponse("post request success")
  #return HttpResponse(json.dumps(my_dict))
  return HttpResponseRedirect('/myaccount')

@login_required
def fetchQuestionPaperJSON(request):
  examid = 0
  
  if request.GET.has_key('examid'):
    examid = request.GET['examid'].strip()

    JSONObj = {
      "qlist" : []
    };

    qlist = ExamQuestions.objects.filter(examname_id=examid)

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


  if request.GET.has_key('ajax'):
    return HttpResponse(json.dumps(JSONObj), content_type="application/json")

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
