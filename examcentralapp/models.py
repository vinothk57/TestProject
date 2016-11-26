from django.db import models
from django.contrib.auth.models import User
from examcentralapp.choices import *

# Create your models here.
class ExamName(models.Model):
  examname = models.TextField(unique=True)
  total_questions = models.IntegerField(max_length=4)
  attempts_allowed = models.IntegerField(max_length=4)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  price = models.DecimalField(max_digits=6, decimal_places=2)
  published = models.BooleanField(default=False)

  def __str__(self):
    return self.examname

class UserExams(models.Model):
  user = models.ForeignKey(User)
  examname = models.ForeignKey(ExamName)
  def __str__(self):
    return '%s, %s' % (self.user.username, self.examname.examname)

#qtype values: 0-multiple choice, 1-true or false, 2- descriptive
class ExamQuestions(models.Model):
  examname = models.ForeignKey(ExamName)
  qno = models.IntegerField(max_length=4)
  question = models.TextField()
  qtype = models.IntegerField(choices=QTYPE_CHOICES, default=1)
  qcategory = models.IntegerField(choices=QCATEGORY_CHOICES, default=1)
  answer = models.TextField(max_length=5000)
  class Admin:
    pass
  def __str__(self):
    return '%s, %s' % (self.question, self.examname.examname)

class OptionA(models.Model):
  examname = models.ForeignKey(ExamName)
  qid = models.IntegerField(max_length=4)
  option = models.TextField(max_length=5000)
  isright = models.BooleanField(default=False)
  class Admin:
    pass
  def __str__(self):
    return '%s, %s, %s, %s' % (self.examname.examname, self.qid, self.option, self.isright)

class OptionB(models.Model):
  examname = models.ForeignKey(ExamName)
  qid = models.IntegerField(max_length=4)
  option = models.TextField(max_length=5000)
  isright = models.BooleanField(default=False)
  class Admin:
    pass
  def __str__(self):
    return '%s, %s, %s, %s' % (self.examname.examname, self.qid, self.option, self.isright)

class OptionC(models.Model):
  examname = models.ForeignKey(ExamName)
  qid = models.IntegerField(max_length=4)
  option = models.TextField(max_length=5000)
  isright = models.BooleanField(default=False)
  class Admin:
    pass
  def __str__(self):
    return '%s, %s, %s, %s' % (self.examname.examname, self.qid, self.option, self.isright)

class OptionD(models.Model):
  examname = models.ForeignKey(ExamName)
  qid = models.IntegerField(max_length=4)
  option = models.TextField(max_length=5000)
  isright = models.BooleanField(default=False)
  class Admin:
    pass
  def __str__(self):
    return '%s, %s, %s, %s' % (self.examname.examname, self.qid, self.option, self.isright)

class ExamSolution(models.Model):
  examname = models.ForeignKey(ExamName)
  qid = models.IntegerField(max_length=4)
  correct_options = models.TextField(max_length=5000)
  explanation = models.TextField(max_length=5000)
  class Admin:
    pass
  def __str__(self):
    return '%s, %s, %s, %s' % (self.examname.examname, self.qid, self.correct_options, self.explanation)

class UserAnswerSheet(models.Model):
  user = models.ForeignKey(User)
  examname = models.ForeignKey(ExamName)
  attemptid = models.IntegerField(max_length=4)
  qid = models.IntegerField(max_length=4)
  user_choices = models.TextField(max_length=5000)
  user_explanation = models.TextField(max_length=5000)
  isright = models.BooleanField(default=False)

  def __str__(self):
    return '%s, %s' % (self.user.username, self.examname.examname)

class UserScoreSheet(models.Model):
  user = models.ForeignKey(User)
  examname = models.ForeignKey(ExamName)
  attemptid = models.IntegerField(max_length=4)
  start_time = models.DateTimeField()
  total_questions = models.IntegerField(max_length=4)
  answered_questions = models.IntegerField(max_length=4)
  correctly_answered = models.IntegerField(max_length=4)
  issubmitted = models.BooleanField(default=False)
  end_time = models.DateTimeField(null=True, blank=True)
  mark = models.DecimalField(max_digits=6, decimal_places=2)

  def __str__(self):
    return '%s, %s, %s, %s, %s, %s, %s' % (self.user.username, self.examname.examname, self.attemptid, self.start_time, self.end_time, self.total_questions, self.mark)

class Tag(models.Model):
  name = models.CharField(max_length=64, unique=True)
  examnames = models.ManyToManyField(ExamName)
  class Admin:
    pass
  def __str__(self):
    return self.name
