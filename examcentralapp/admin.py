from django.contrib import admin
from examcentralapp.models import *

class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'country', 'phone', 'address', 'profilepic')
    list_filter = ('user', 'city', 'country', 'phone')
    ordering = ('user', 'country', 'city')
    search_fields = ('user', 'country', 'city')

class UserExamsAdmin(admin.ModelAdmin):
    list_display = ('user', 'examname')
    list_filter = ('user', 'examname')
    ordering = ('user', )
    search_fields = ('user', 'examname')

class ExamQuestionsAdmin(admin.ModelAdmin):
    list_display = ('examname', 'qno', 'question', 'haspic', 'hasdirection', 'qtype', 'qcategory', 'answer')
    list_filter = ('examname', 'qno')
    ordering = ('qno',)
    search_fields = ('question', 'examname')

class QuestionInfoAdmin(admin.ModelAdmin):
    list_display = ('examname', 'qid', 'pic', 'direction')
    list_filter = ('examname', 'qid')
    ordering = ('examname',)
    search_fields = ('examname', 'direction')

class OptionAAdmin(admin.ModelAdmin):
    list_display = ('examname', 'qid', 'option', 'isright')
    list_filter = ('examname', 'qid', 'option', 'isright')
    ordering = ('examname',)
    search_fields = ('qid',)

class OptionBAdmin(admin.ModelAdmin):
    list_display = ('examname', 'qid', 'option', 'isright')
    list_filter = ('examname', 'qid', 'option', 'isright')
    ordering = ('examname',)
    search_fields = ('qid',)

class OptionCAdmin(admin.ModelAdmin):
    list_display = ('examname', 'qid', 'option', 'isright')
    list_filter = ('examname', 'qid', 'option', 'isright')
    ordering = ('examname',)
    search_fields = ('qid',)

class OptionDAdmin(admin.ModelAdmin):
    list_display = ('examname', 'qid', 'option', 'isright')
    list_filter = ('examname', 'qid', 'option', 'isright')
    ordering = ('examname',)
    search_fields = ('qid',)

class ExamSolutionAdmin(admin.ModelAdmin):
    list_display = ('examname', 'qid', 'correct_options', 'explanation')
    list_filter = ('examname', 'qid')
    ordering = ('examname',)
    search_fields = ('examname', 'qid')

class UserAnswerSheetAdmin(admin.ModelAdmin):
    list_display = ('user', 'examname', 'attemptid', 'qid', 'user_choices')
    list_filter = ('user', 'examname', 'qid')
    ordering = ('user', 'examname', 'attemptid')
    search_fields = ('user', 'examname', 'qid')

class UserScoreSheetAdmin(admin.ModelAdmin):
    list_display = ('user', 'examname', 'attemptid', 'start_time', 'end_time', 'mark', 'answered_questions', 'correctly_answered')
    list_filter = ('user', 'examname', 'attemptid', 'issubmitted')
    ordering = ('user', 'examname', 'attemptid')
    search_fields = ('user', 'examname')

# Register your models here.
admin.site.register(ExamName)
admin.site.register(UserExams, UserExamsAdmin)
admin.site.register(ExamQuestions, ExamQuestionsAdmin)
admin.site.register(QuestionInfo, QuestionInfoAdmin)
admin.site.register(OptionA, OptionAAdmin)
admin.site.register(OptionB, OptionBAdmin)
admin.site.register(OptionC, OptionCAdmin)
admin.site.register(OptionD, OptionDAdmin)
admin.site.register(ExamSolution, ExamSolutionAdmin)
admin.site.register(UserAnswerSheet, UserAnswerSheetAdmin)
admin.site.register(UserScoreSheet, UserScoreSheetAdmin)
admin.site.register(UserDetails, UserDetailsAdmin)
