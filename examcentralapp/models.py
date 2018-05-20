from django.db import models
from django.contrib.auth.models import User
from examcentralapp.choices import *
from examcentralapp.storage import OverwriteStorage
from tinymce.models import HTMLField

def user_directory_path(instance, filename):
  return 'user_%s/profilepic/profile.png' % (instance.user.id)

def qtn_directory_path(instance, filename):
  return '%s/%s' % (instance.examname, filename)

# Create your models here.
class UserDetails(models.Model):
  user = models.ForeignKey(User)
  address = models.TextField(max_length=5000, null=True, blank=True)
  city = models.TextField(max_length=500, null=True, blank=True)
  country = models.TextField(max_length=500, null=True, blank=True)
  pincode = models.BigIntegerField(null=True, blank=True)
  phone = models.CharField(max_length=30, null=True, blank=True)
  aboutme = models.TextField(max_length=5000, null=True, blank=True)
  profilepic = models.FileField(upload_to=user_directory_path, storage=OverwriteStorage(), null=True, blank=True)
  def __str__(self):
    return '%s, %s, %s, %s' % (self.user.username, self.address, self.city, self.country)

class ExamName(models.Model):
  examname = models.CharField(max_length=150, unique=True)
  total_questions = models.IntegerField()
  attempts_allowed = models.IntegerField()
  duration = models.IntegerField()
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  mark_per_qtn = models.IntegerField()
  negative_per_qtn = models.DecimalField(max_digits=6, decimal_places=2)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  published = models.BooleanField(default=False)

  def __str__(self):
    return self.examname

class ExamSectionInfo(models.Model):
  examname = models.ForeignKey(ExamName, on_delete=models.CASCADE)
  section_no = models.IntegerField()
  section_name = models.CharField(max_length=100)
  section_qcount = models.IntegerField()
  section_mark_per_qtn = models.IntegerField()
  section_negative_per_qtn = models.DecimalField(max_digits=6, decimal_places=2)

  def __str__(self):
    return '%s, %s' % (self.examname, self.section_name)

class UserExams(models.Model):
  user = models.ForeignKey(User)
  examname = models.ForeignKey(ExamName)
  def __str__(self):
    return '%s, %s' % (self.user.username, self.examname.examname)

class UserExamAttemptInfo(models.Model):
    userexam = models.ForeignKey(UserExams)
    attempt_available = models.IntegerField()
    def __str__(self):
        return '%s, %s, %s' % (self.userexam.user.username, self.userexam.examname.examname, self.attempt_available)

#qtype values: 0-multiple choice, 1-true or false, 2- descriptive
class ExamQuestions(models.Model):
  examname = models.ForeignKey(ExamName)
  qno = models.IntegerField()
  question = models.TextField()
  qtype = models.IntegerField(choices=QTYPE_CHOICES, default=1)
  qcategory = models.IntegerField(choices=QCATEGORY_CHOICES, default=1)
  haspic = models.BooleanField(default=False)
  hasdirection = models.BooleanField(default=False)
  answer = models.TextField(max_length=5000)
  class Admin:
    pass
  def __str__(self):
    return '%s, %s' % (self.question, self.examname.examname)

class QuestionInfo(models.Model):
  examname = models.ForeignKey(ExamName)
  qid = models.IntegerField()
  pic = models.FileField(upload_to=qtn_directory_path, null=True, blank=True)
  #direction = models.TextField()
  direction = HTMLField()
  class Admin:
    pass
  def __str__(self):
    return '%s, %s, %s' % (self.examname.examname, self.qid, self.direction)

class OptionA(models.Model):
  examname = models.ForeignKey(ExamName)
  qid = models.IntegerField()
  option = models.TextField(max_length=5000)
  isright = models.BooleanField(default=False)
  class Admin:
    pass
  def __str__(self):
    return '%s, %s, %s, %s' % (self.examname.examname, self.qid, self.option, self.isright)

class OptionB(models.Model):
  examname = models.ForeignKey(ExamName)
  qid = models.IntegerField()
  option = models.TextField(max_length=5000)
  isright = models.BooleanField(default=False)
  class Admin:
    pass
  def __str__(self):
    return '%s, %s, %s, %s' % (self.examname.examname, self.qid, self.option, self.isright)

class OptionC(models.Model):
  examname = models.ForeignKey(ExamName)
  qid = models.IntegerField()
  option = models.TextField(max_length=5000)
  isright = models.BooleanField(default=False)
  class Admin:
    pass
  def __str__(self):
    return '%s, %s, %s, %s' % (self.examname.examname, self.qid, self.option, self.isright)

class OptionD(models.Model):
  examname = models.ForeignKey(ExamName)
  qid = models.IntegerField()
  option = models.TextField(max_length=5000)
  isright = models.BooleanField(default=False)
  class Admin:
    pass
  def __str__(self):
    return '%s, %s, %s, %s' % (self.examname.examname, self.qid, self.option, self.isright)

class OptionE(models.Model):
  examname = models.ForeignKey(ExamName)
  qid = models.IntegerField()
  option = models.TextField(max_length=5000)
  isright = models.BooleanField(default=False)
  class Admin:
    pass
  def __str__(self):
    return '%s, %s, %s, %s' % (self.examname.examname, self.qid, self.option, self.isright)

class ExamSolution(models.Model):
  examname = models.ForeignKey(ExamName)
  qid = models.IntegerField()
  correct_options = models.TextField(max_length=5000)
  explanation = models.TextField(max_length=5000)
  class Admin:
    pass
  def __str__(self):
    return '%s, %s, %s, %s' % (self.examname.examname, self.qid, self.correct_options, self.explanation)

class UserAnswerSheet(models.Model):
  user = models.ForeignKey(User)
  examname = models.ForeignKey(ExamName)
  attemptid = models.IntegerField()
  qid = models.IntegerField()
  user_choices = models.TextField(max_length=5000)
  user_explanation = models.TextField(max_length=5000)
  isright = models.BooleanField(default=False)

  def __str__(self):
    return '%s, %s' % (self.user.username, self.examname.examname)

class UserScoreSheet(models.Model):
  user = models.ForeignKey(User)
  examname = models.ForeignKey(ExamName)
  attemptid = models.IntegerField()
  start_time = models.DateTimeField()
  total_questions = models.IntegerField()
  answered_questions = models.IntegerField()
  correctly_answered = models.IntegerField()
  issubmitted = models.BooleanField(default=False)
  end_time = models.DateTimeField(null=True, blank=True)
  mark = models.DecimalField(max_digits=6, decimal_places=2)

  def __str__(self):
    return '%s, %s, %s, %s, %s, %s, %s' % (self.user.username, self.examname.examname, self.attemptid, self.start_time, self.end_time, self.total_questions, self.mark)

class UserSectionScore(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  examname = models.ForeignKey(ExamName, on_delete=models.CASCADE)
  attemptid = models.IntegerField()
  section_no = models.IntegerField()
  section_answered_questions = models.IntegerField()
  section_correctly_answered = models.IntegerField()
  section_score = models.DecimalField(max_digits=6, decimal_places=2)

  def __str__(self):
    return '%s, %s, %s, %s' % (self.user.username, self.examname.examname, self.attemptid, self.section_score)

class Tag(models.Model):
  name = models.CharField(max_length=64, unique=True)
  examnames = models.ManyToManyField(ExamName)
  class Admin:
    pass
  def __str__(self):
    return self.name
