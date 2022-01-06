from django.forms import ModelForm
from .models import CustomerFeedback


class CustomerFeedbackForm(ModelForm):
    class Meta:
        model = CustomerFeedback
        fields = ['fullname','customer_type','person_transacted','rate1','rate2','rate3','rate4', 'rate5','comment',]

