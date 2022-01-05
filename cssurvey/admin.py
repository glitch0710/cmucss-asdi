from django.contrib import admin
from .models import CustomerFeedback

class CustomerFeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)

admin.site.register(CustomerFeedback, CustomerFeedbackAdmin)
