from django.forms import ModelForm
from .models import TbCssrespondents, TbCssrespondentsDetails, TbQuestions, TbEmployees


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


class TbQuestionsForm(ModelForm):
    class Meta:
        model = TbQuestions
        fields = ['survey_question', 'display_status']


class TbEmployeesForm(ModelForm):
    class Meta:
        model = TbEmployees
        fields = ['office_id', 'job_position', 'user', 'middlename', 'image']

