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

class UserExamAttemptInfoAdmin(admin.ModelAdmin):
    list_display = ('userexam', 'attempt_available')
    list_filter = ('userexam', 'attempt_available')
    ordering = ('userexam',)
    search_fields = ('userexam',)

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

class OptionEAdmin(admin.ModelAdmin):
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

class ExamSectionInfoAdmin(admin.ModelAdmin):
    list_display = ('examname', 'section_no', 'section_name', 'section_qcount', 'section_mark_per_qtn', 'section_negative_per_qtn')
    list_filter = ('examname', 'section_name')
    ordering = ('examname', 'section_no')
    search_fields = ('examname', 'section_name')

class UserSectionScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'examname', 'attemptid', 'section_no', 'section_answered_questions', 'section_correctly_answered', 'section_score')
    list_filter = ('examname', 'user', 'attemptid')
    ordering = ('examname', 'user', 'attemptid', 'section_no')
    search_fields = ('user', 'examname', 'attemptid', 'section_no')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'pic')
    list_filter = ('title', 'pic')
    ordering = ('time', 'title')
    search_fields = ('title', 'text')

class TransactionDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'txn_id', 'productinfo', 'txn_status')
    list_filter = ('user', 'productinfo')
    ordering = ('time', 'user', 'productinfo')
    search_fields = ('txn_id', 'user', 'productinfo')

# Register your models here.
admin.site.register(ExamName)
admin.site.register(UserExams, UserExamsAdmin)
admin.site.register(ExamQuestions, ExamQuestionsAdmin)
admin.site.register(QuestionInfo, QuestionInfoAdmin)
admin.site.register(OptionA, OptionAAdmin)
admin.site.register(OptionB, OptionBAdmin)
admin.site.register(OptionC, OptionCAdmin)
admin.site.register(OptionD, OptionDAdmin)
admin.site.register(OptionE, OptionEAdmin)
admin.site.register(ExamSolution, ExamSolutionAdmin)
admin.site.register(UserAnswerSheet, UserAnswerSheetAdmin)
admin.site.register(UserScoreSheet, UserScoreSheetAdmin)
admin.site.register(UserDetails, UserDetailsAdmin)
admin.site.register(UserExamAttemptInfo, UserExamAttemptInfoAdmin)
admin.site.register(ExamSectionInfo, ExamSectionInfoAdmin)
admin.site.register(UserSectionScore, UserSectionScoreAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(TransactionDetail, TransactionDetailAdmin)

