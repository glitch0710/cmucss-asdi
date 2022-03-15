from django.forms import ModelForm
from .models import TbCssrespondents, TbCssrespondentsDetails, TbQuestions


class TbCssrespondentsForm(ModelForm):
    class Meta:
        model = TbCssrespondents
        fields = ['respondentname',
                  'respondenttype',
                  'employee_id',
                  'coverageid',
                  'respondedofficeid',
                  'comments',]


class TbCssrespondentsDetailsForm(ModelForm):
    class Meta:
        model = TbCssrespondentsDetails
        fields = ['qid',
                  'respondentid',
                  'rating',]

