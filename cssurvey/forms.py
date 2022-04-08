from django.forms import ModelForm, Select, Textarea, TextInput, CheckboxInput
from .models import TbCssrespondents, TbCssrespondentsDetails, TbQuestions, TbEmployees, TbCmuoffices
from django.contrib.auth.models import User


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
        fields = ['survey_question', 'display_status',]


class TbEmployeesForm(ModelForm):
    class Meta:
        model = TbEmployees
        fields = ['office_id', 'job_position', 'user', 'middlename', 'image',]
        widgets = {
            'office_id': Select(attrs={
                'class': "form-control",
                'id': "office_id",
                'name': "office_id",
            })
        }


class UserChangeUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]


class UserProfileUpdateForm(ModelForm):
    class Meta:
        model = TbEmployees
        fields = ['job_position', 'office_id',]


class TbCmuOfficesForm(ModelForm):
    class Meta:
        model = TbCmuoffices
        fields = ['officename','officecode','is_active',]
        widgets = {
            'officename': Textarea(attrs={
                'class': "form-control",
                'id': "officename",
                'name': "officename",
            }),
            'officecode': TextInput(attrs={
                'class': "form-control",
                'id': "officecode",
                'name': "officecode",
            }),
            'is_active': CheckboxInput(attrs={
                'class': "custom-control-input",
                'id': "is_active",
                'name': "is_active",
                'type': "checkbox"
            }),
        }


class TbCmuOfficesAddForm(ModelForm):
    class Meta:
        model = TbCmuoffices
        fields = ['officename', 'officecode',]
        widgets = {
            'officename': Textarea(attrs={
                'class': "form-control",
                'id': "officename",
                'name': "officename",
            }),
            'officecode': TextInput(attrs={
                'class': "form-control",
                'id': "officecode",
                'name': "officecode",
            }),
        }
