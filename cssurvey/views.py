from django.shortcuts import render, redirect, get_object_or_404
from .models import TbQuestions, TbCoverage, TbCmuoffices, TbCssrespondentsDetails, TbEmployees
from .forms import TbCssrespondentsForm, TbCssrespondentsDetailsForm, TbCssrespondents, TbQuestionsForm, TbEmployeesForm, UserChangeUpdateForm, UserProfileUpdateForm, TbCmuOfficesForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'cssurvey/loginuser.html', {'form': AuthenticationForm()})
    else:
        try:
            user = authenticate(request,
                                username=request.POST['username'],
                                password=request.POST['password'],)

            if user is None:
                return render(request,
                              'cssurvey/loginuser.html',
                              {'form': AuthenticationForm(),
                               'error': 'Email and password do not match or this account is inactive. '
                                        'Please try again!'})
            else:
                login(request, user)
                return redirect('controlpanel')
        except ValidationError:
            return render(request,
                          'cssurvey/loginuser.html',
                          {'form': AuthenticationForm(),
                           'error': 'This account is inactive.'})


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginuser')


def index(request):
    return render(request, 'cssurvey/index.html')


def customersurvey(request):
    questions = TbQuestions.objects.filter(display_status=1)

    if request.method == 'GET':
        if request.GET.get('office'):
            # implement this when finished with link generation for css
            officeno = request.GET.get('office')
        else:
            # default for now
            officeno = 35

        officename = TbCmuoffices.objects.get(officeid=officeno)
        return render(request, 'cssurvey/customersurvey.html', {'questions': questions,
                                                                'office': officename,
                                                                'form': TbCssrespondentsForm,
                                                                'form1': TbCssrespondentsDetailsForm})
    else:
        try:
            if request.GET.get('office'):
                # implement this when finished with link generation for css
                officeno = request.GET.get('office')
            else:
                # default for now
                officeno = 35

            if request.GET.get('employee'):
                # implement this when finished with link generation for css
                employee = request.GET.get('employee')
            else:
                # default for now
                employee = 0

            form = TbCssrespondentsForm(request.POST)
            newcss = form.save(commit=False)

            newcss.employee_id = employee
            newcss.coverageid = TbCoverage.objects.latest('coverageid')
            newcss.respondedofficeid = TbCmuoffices.objects.get(officeid=officeno)
            newcss.save()

            # get last id inserted
            last_id = newcss.respondentid

            css_details = request.POST
            for question in questions:
                rate = css_details.get('rate' + str(question.qid))
                if int(rate) > 5:
                    raise ValueError
                elif int(rate) <= 0:
                    raise ValueError

                TbCssrespondentsDetails.objects.create(qid=TbQuestions.objects.get(qid=question.qid),
                                                       respondentid=TbCssrespondents.objects.get(respondentid=last_id),
                                                       rating=rate)

            return redirect('submitcss')
        except ValueError:
            TbCssrespondents.objects.filter(respondentid=last_id).delete()
            return render(
                request,
                'cssurvey/customersurvey.html',
                {'questions': questions, 'form': TbCssrespondentsForm, 'error': 'Bad data passed in. Please try again!'}
            )


def submitcss(request):
    return render(request, 'cssurvey/submitcss.html')


@login_required
def controlpanel(request):
    return render(request, 'cssurvey/controlpanel.html')


@login_required
def questions(request):
    if request.method == 'GET':
        active_questions = TbQuestions.objects.filter(display_status=1)
        inactive_questions = TbQuestions.objects.filter(display_status=0)
        return render(request, 'cssurvey/questions.html', {'active': active_questions,
                                                           'inactive': inactive_questions,
                                                           'searched': '',})

    else:
        search_data = request.POST
        return_question_data = TbQuestions.objects.filter(survey_question__icontains=search_data.get('searchQuestion'))

        return render(request, 'cssurvey/questions.html', {'active': '',
                                                           'inactive': '',
                                                           'searched': return_question_data,})


@login_required
def viewquestion(request, question_pk):
    question = get_object_or_404(TbQuestions, pk=question_pk)
    if request.method == 'GET':
        form = TbQuestionsForm(instance=question)
        return render(request, 'cssurvey/viewquestion.html', {'question': question, 'form': form})
    else:
        try:
            form = TbQuestionsForm(request.POST, instance=question)
            if form.is_valid():
                form.save()
                return redirect('questions')
            else:
                raise ValueError
        except ValueError:
            return render(request, 'cssurvey/viewquestion.html', {'question': question,
                                                                  'form': form,
                                                                  'error': 'Bad data passed in!'})


@login_required
def create_question(request):
    if request.method == 'POST':
        try:
            new_question = TbQuestionsForm(request.POST)
            if new_question.is_valid():
                print(request.POST['survey_question'])
                if request.POST['survey_question'] is None or request.POST['survey_question'] == '':
                    raise ValueError
                else:
                    new_question.save()
                    return redirect('questions')
            else:
                active_questions = TbQuestions.objects.filter(display_status=1)
                inactive_questions = TbQuestions.objects.filter(display_status=0)
                return render(request, 'cssurvey/questions.html', {'active': active_questions,
                                                                   'inactive': inactive_questions,
                                                                   'searched': '',
                                                                   'error': 'Bad data passed in. Please try again!'})
        except ValueError:
            active_questions = TbQuestions.objects.filter(display_status=1)
            inactive_questions = TbQuestions.objects.filter(display_status=0)
            return render(request, 'cssurvey/questions.html', {'active': active_questions,
                                                               'inactive': inactive_questions,
                                                               'searched': '',
                                                               'error': 'Bad data passed in. Please try again!'})


@login_required
def delete_question(request, question_pk):
    del_question = get_object_or_404(TbQuestions, pk=question_pk)
    if request.method == 'POST':
        if del_question.display_status:
            return redirect('viewquestion', question_pk=del_question.qid)
        else:
            del_question.delete()
            return redirect('questions')


@login_required
def user_accounts(request):
    form_profile = TbEmployeesForm()
    userid = request.user.id
    if request.method == 'GET':
        user = get_user_model()
        users = user.objects.all()

        return render(request, 'cssurvey/useraccounts.html', {'form': UserCreationForm(),
                                                              'form1': UserChangeForm(),
                                                              'users': users,
                                                              'form_profile': form_profile,
                                                              'userid': userid})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                new_user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                new_user.last_name = request.POST['last_name']
                new_user.first_name = request.POST['first_name']
                new_user.email = request.POST['email']

                if request.POST['office_id'] == 0 or request.POST['office_id'] == '':
                    raise ValueError
                else:
                    office_id = request.POST['office_id']

                # save user
                new_user.save()
                # save user profile
                TbEmployees.objects.create(office_id=TbCmuoffices.objects.get(officeid=office_id),
                                           job_position=request.POST['job_position'],
                                           user=User.objects.get(id=User.objects.latest('id').id))
                return redirect('user_accounts')
            except IntegrityError:
                user = get_user_model()
                users = user.objects.all()
                return render(request, 'cssurvey/useraccounts.html', {'form': UserCreationForm(),
                                                                      'form1': UserChangeForm(),
                                                                      'users': users,
                                                                      'form_profile': form_profile,
                                                                      'error': 'That username has already been taken.'
                                                                               ' Please choose a new username',
                                                                      'userid': userid})
            except ValueError:
                user = get_user_model()
                users = user.objects.all()
                return render(request, 'cssurvey/useraccounts.html', {'form': UserCreationForm(),
                                                                      'form1': UserChangeForm(),
                                                                      'users': users,
                                                                      'form_profile': form_profile,
                                                                      'error': 'Bad data passed in. Please try again.',
                                                                      'userid': userid})

        else:
            user = get_user_model()
            users = user.objects.all()

            return render(request, 'cssurvey/useraccounts.html', {'form': UserCreationForm(),
                                                                  'form1': UserChangeForm(),
                                                                  'users': users,
                                                                  'form_profile': form_profile,
                                                                  'error': 'Passwords did not match',
                                                                  'userid': userid})


@login_required
def view_user(request, user_pk):
    user_details = get_object_or_404(User, pk=user_pk)
    user_profile = get_object_or_404(TbEmployees, user=user_pk)
    form_profile = TbEmployeesForm(instance=user_profile)
    if request.method == 'GET':
        return render(request, 'cssurvey/viewuser.html', {'form_profile': form_profile,
                                                          'profile': user_details,
                                                          'profile_details': user_profile})
    else:
        try:
            user_form = UserChangeUpdateForm(request.POST, instance=user_details)
            details_form = UserProfileUpdateForm(request.POST, instance=user_profile)

            if user_form.is_valid() and details_form.is_valid():
                user_form.username = request.POST['username']
                user_form.first_name = request.POST['first_name']
                user_form.last_name = request.POST['last_name']
                user_form.email = request.POST['email']
                details_form.job_position = request.POST['job_position']
                details_form.office_id = TbCmuoffices.objects.get(officeid=request.POST['office_id'])

                user_form.save()
                details_form.save()
                return render(request, 'cssurvey/viewuser.html', {'form_profile': form_profile,
                                                                  'profile': user_details,
                                                                  'profile_details': user_profile,
                                                                  'success': 'Profile update successfully saved'})
            else:
                return render(request, 'cssurvey/viewuser.html', {'form_profile': form_profile,
                                                                  'profile': user_details,
                                                                  'profile_details': user_profile,
                                                                  'error': 'Form did not validate. Please try again'})
        except ValueError:
            return render(request, 'cssurvey/viewuser.html', {'form_profile': form_profile,
                                                              'profile': user_details,
                                                              'profile_details': user_profile,
                                                              'error': 'Bad data passed in. Please try again'})


@login_required()
def change_password(request, user_pk):
    user_details = get_object_or_404(User, pk=user_pk)
    if request.method == 'GET':
        return render(request, 'cssurvey/changepassword.html', {'profile': user_details,})
    else:
        try:
            new_password = request.POST['new_password1'].strip()
            confirm_password = request.POST['new_password2'].strip()

            if new_password == '':
                raise ValueError

            if new_password == confirm_password:
                user_details.set_password(new_password)
                user_details.save()
                return render(request, 'cssurvey/changepassword.html', {'profile': user_details,
                                                                        'success': 'User\'s password was successfully updated.',
                                                                        })
            else:
                return render(request, 'cssurvey/changepassword.html', {'profile': user_details,
                                                                        'error': 'Passwords do not match! Please try again.',
                                                                        })
        except ValueError:
            return render(request, 'cssurvey/changepassword.html', {'profile': user_details,
                                                                    'error': 'Bad data passed in. Please try again.',
                                                                    })

    # change password for user
    # user_details = get_object_or_404(User, pk=user_pk)
    # if request.method == 'GET':
    #     return render(request, 'cssurvey/changepassword.html', {'profile': user_details})
    # else:
    #     form = PasswordChangeForm(user_details, request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         update_session_auth_hash(request, user)
    #         return render(request, 'cssurvey/changepassword.html', {'profile': user_details,
    #                                                                 'success': 'Password was successfully updated'})


@login_required
def deactivate_user(request, user_pk):
    deactivate = get_object_or_404(User, pk=user_pk)
    deactivate.is_active = 0
    deactivate.save()
    return redirect('user_accounts')


@login_required
def reactivate_user(request, user_pk):
    reactivate = get_object_or_404(User, pk=user_pk)
    reactivate.is_active = 1
    reactivate.save()
    return redirect('user_accounts')


@login_required
def offices(request):
    if request.method == 'GET':
        all_offices = TbCmuoffices.objects.all()
        return render(request, 'cssurvey/offices.html', {'offices': all_offices})
    else:
        pass


@login_required
def view_office(request, office_pk):
    if request.method == 'GET':
        office = get_object_or_404(TbCmuoffices, pk=office_pk)
        form = TbCmuOfficesForm(instance=office)
        return render(request, 'cssurvey/viewoffice.html', {'office': office,
                                                            'form': form})
    else:
        office = get_object_or_404(TbCmuoffices, pk=office_pk)
        form = TbCmuOfficesForm(instance=office)
        office_form = TbCmuOfficesForm(request.POST, instance=office)
        try:
            if office_form.is_valid():
                office_form.save()
                return redirect('view_office', office_pk=office.officeid)
            else:
                return render(request, 'cssurvey/viewoffice.html', {'office': office,
                                                                    'form': form,
                                                                    'error': 'Form did not validate, please try again.'})
        except ValueError:
            return render(request, 'cssurvey/viewoffice.html', {'office': office,
                                                                'form': form,
                                                                'error': 'Bad data passed in. Please try again.'})


@login_required
def office_staff(request, office_pk):
    if request.method == 'GET':
        office = get_object_or_404(TbCmuoffices, pk=office_pk)
        staff = User.objects.filter(tbemployees__office_id=office)
        return render(request, 'cssurvey/officestaff.html', {'office': office,
                                                             'staff': staff})
    else:
        pass

