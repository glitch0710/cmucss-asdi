from django.contrib import admin
from .models import CustomerFeedback, Question


class CustomerFeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)


class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)


admin.site.register(CustomerFeedback, CustomerFeedbackAdmin)
admin.site.register(Question, QuestionAdmin)
