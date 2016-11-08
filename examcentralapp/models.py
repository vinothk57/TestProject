from django.db import models
from django.contrib.auth.models import User
from examcentralapp.choices import *

# Create your models here.
class ExamName(models.Model):
  examname = models.TextField(unique=True)
  total_questions = models.IntegerField(max_length=4)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  price = models.DecimalField(max_digits=6, decimal_places=2)
  published = models.BooleanField(default=False)

  def __str__(self):
    return self.examname

class UserExams(models.Model):
  user = models.ForeignKey(User)
  examname = models.ForeignKey(ExamName)
  class Admin:
    pass
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
  examid = models.IntegerField()
  qid = models.IntegerField(max_length=4)
  option = models.TextField(max_length=5000)
  isright = models.BooleanField(default=False)
  class Admin:
    pass
  def __str__(self):
    return '%s, %s, %s, %s' % (self.examid, self.qid, self.option, self.isright)

class OptionB(models.Model):
  examid = models.IntegerField()
  qid = models.IntegerField(max_length=4)
  option = models.TextField(max_length=5000)
  isright = models.BooleanField(default=False)
  class Admin:
    pass
  def __str__(self):
    return '%s, %s, %s, %s' % (self.examid, self.qid, self.option, self.isright)

class OptionC(models.Model):
  examid = models.IntegerField()
  qid = models.IntegerField(max_length=4)
  option = models.TextField(max_length=5000)
  isright = models.BooleanField(default=False)
  class Admin:
    pass
  def __str__(self):
    return '%s, %s, %s, %s' % (self.examid, self.qid, self.option, self.isright)

class OptionD(models.Model):
  examid = models.IntegerField()
  qid = models.IntegerField(max_length=4)
  option = models.TextField(max_length=5000)
  isright = models.BooleanField(default=False)
  class Admin:
    pass
  def __str__(self):
    return '%s, %s, %s, %s' % (self.examid, self.qid, self.option, self.isright)

class Tag(models.Model):
  name = models.CharField(max_length=64, unique=True)
  examnames = models.ManyToManyField(ExamName)
  class Admin:
    pass
  def __str__(self):
    return self.name
