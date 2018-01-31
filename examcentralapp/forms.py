from django import forms
from django.contrib.auth.forms import AuthenticationForm 
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from examcentralapp.choices import *

#SignUp page Form
class RegistrationForm(forms.Form):
  username = forms.CharField(label='Username* ', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
  firstname = forms.CharField(label='First Name* ', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
  lastname = forms.CharField(label='Last Name ', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}), required=False)
  email = forms.EmailField(label='Email* ', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
  password1 = forms.CharField(
     label='Password* ',
     widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
  )
  password2 = forms.CharField(
     label='Confirm Password* ',
     widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
  )

  def clean_password2(self):
    if 'password1' in self.cleaned_data:
      password1 = self.cleaned_data['password1']
      password2 = self.cleaned_data['password2']
      if password1 == password2:
        return password2
    raise forms.ValidationError('Passwords do not match.')

  def clean_username(self):
    username = self.cleaned_data['username']
    if not re.search(r'^\w+$', username):
      raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
    try:
      User.objects.get(username=username)
    except ObjectDoesNotExist:
      return username
    raise forms.ValidationError('Username is already taken.')

  def clean_email(self):
    email = self.cleaned_data['email']
    try:
      User.objects.get(email=email)
    except ObjectDoesNotExist:
      return email
    raise forms.ValidationError('Email already registered.')


class UpdateProfileForm(forms.Form):
  username = forms.CharField(label='Username ', max_length=30, widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'placeholder': 'Username'}))
  firstname = forms.CharField(label='First Name ', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
  lastname = forms.CharField(label='Last Name ', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}), required=False)
  email = forms.EmailField(label='Email ', widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'placeholder': 'Email'}))
  address = forms.CharField(label='Address ', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Door No./Building/Street Name'}), required=False)
  city = forms.CharField(label='City', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}), required=False)
  country = forms.CharField(label='Country', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}), required=False)
  pincode = forms.IntegerField(
    label='PIN Code', min_value = 1,
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PIN/ZIP Code'}), required=False
  )
  phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$', required=False)
  aboutme = forms.CharField(label='About Me', max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell everyone how cool you are!'}), required=False)

  def clean_phone(self):
    phone = self.cleaned_data['phone']
    if phone:
      if not re.search(r'^[0-9\+]+$', phone):
        raise forms.ValidationError('Phone number can only contain numeric characters and +.')

#  def clean_pincode(self):
#    pincode = self.cleaned_data['pincode']
#    if not re.search(r'^[0-9\+]+$', pincode):
#      raise forms.ValidationError('PIN/ZIP code can only contain numeric characters')


# If you don't do this you cannot use Bootstrap CSS
#Login page - Default form modified
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder': 'Username/Email'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder': 'Password'}))

#Creating Exam Form
class ExamDetailsSaveForm(forms.Form):
  examname = forms.CharField(
    label='',
    widget=forms.TextInput(attrs={'id': 'examname', 'class': 'form-control', 'placeholder': 'Exam Name'})
  )
  total_questions = forms.IntegerField(
    label='', min_value = 1,
    widget=forms.TextInput(attrs={'id': 'total-questions', 'class': 'form-control', 'placeholder': 'Total Questions'})
  )
  attempts_allowed = forms.IntegerField(
    label='', min_value = 1,
    widget=forms.TextInput(attrs={'id': 'attempts-allowed', 'class': 'form-control', 'placeholder': 'Attempts allowed per user'})
  )

  duration = forms.IntegerField(label='', min_value = 1, widget=forms.TextInput(attrs={'id': 'duration', 'class': 'form-control', 'placeholder': 'Exam duration in minutes'}))

  start_time = forms.DateTimeField(label='', widget=forms.DateTimeInput(attrs={'id': 'start-time', 'class': 'form-control', 'placeholder': 'Start Time'}))
  end_time = forms.DateTimeField(label ='', widget=forms.DateTimeInput(attrs={'id': 'end-time', 'class': 'form-control', 'placeholder': 'End Time'}))
  price = forms.FloatField(
    label='', min_value = 0,
    widget=forms.TextInput(attrs={'id': 'price', 'class': 'form-control', 'placeholder': 'Price'})
  )
  #published = forms.BooleanField(label='Publish Exam', initial=False)

  tags = forms.CharField(
    label='',
    required=False,
    widget=forms.TextInput(attrs={'id': 'tags', 'class': 'form-control', 'placeholder': 'Space separated tags'})
  )

class SearchForm(forms.Form):
  query = forms.CharField(
      label='Enter a keyword to search for exam:',
      widget=forms.TextInput(attrs={'size': 32, 'placeholder': 'Search Exam'})
  )

  def clean_query(self):
    query = self.cleaned_data['query']
    if not query:
      raise forms.ValidationError('Empty search')
    else:
      return query

#Creating Question Form
class QuestionDetailsSaveForm(forms.Form):
  qno = forms.IntegerField(label='', min_value=1,
          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Question Number'})
        )
  question = forms.CharField(label='',
          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Question'})
        )
  qtype = forms.ChoiceField(choices=QTYPE_CHOICES, required=False)
  qcategory = forms.ChoiceField(choices=QCATEGORY_CHOICES)
  optionA = forms.CharField(label='',
          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option A'})
        )
  isOptionA = forms.BooleanField(label='Is Option A correct', initial=False, required=False)
  optionB = forms.CharField(label='',
          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option B'})
        )
  isOptionB = forms.BooleanField(label='Is Option B correct', initial=False, required=False)
  optionC = forms.CharField(label='',
          required=False,
          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option C'})
        )
  isOptionC = forms.BooleanField(label='Is Option C correct', initial=False, required=False)
  optionD = forms.CharField(label='',
          required=False,
          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option D'})
        )
  isOptionD = forms.BooleanField(label='Is Option D correct', initial=False, required=False)
  answer = forms.CharField(
     label='',
     widget=forms.TextInput(attrs={'id': 'answer', 'class': 'form-control', 'placeholder': 'Enter Answer'})
   )

class DocumentForm(forms.Form):
  docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email or Username'}))

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }

    new_password1 = forms.CharField(label='',
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'}))
    new_password2 = forms.CharField(label='',
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter new password'}))
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2
