from django.shortcuts import render, redirect, get_object_or_404
from .models import TbQuestions, TbCoverage, TbCmuoffices, TbCssrespondentsDetails, TbEmployees
from .forms import TbCssrespondentsForm, TbCssrespondentsDetailsForm, TbCssrespondents, TbQuestionsForm, TbEmployeesForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'cssurvey/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'],)
        if user is None:
            return render(request,
                          'cssurvey/loginuser.html',
                          {'form': AuthenticationForm(),
                           'error': 'Email and password do not match. Please try again!'})
        else:
            login(request, user)
            return redirect('controlpanel')


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
            form.save()
            return redirect('questions')
        except ValueError:
            return render(request, 'cssurvey/viewquestion.html', {'question': question,
                                                                  'form': form,
                                                                  'error': 'Bad data passed in!'})


@login_required
def user_accounts(request):
    if request.method == 'GET':
        user = get_user_model()
        users = user.objects.all()

        return render(request, 'cssurvey/useraccounts.html', {'form': UserCreationForm(),
                                                              'form1': UserChangeForm(),
                                                              'users': users})
    else:
        # data = request.POST
        if request.POST['password1'] == request.POST['password2']:
            try:
                new_user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                new_user.last_name = request.POST['last_name']
                new_user.first_name = request.POST['first_name']
                new_user.email = request.POST['email']
                new_user.save()

                TbEmployees.objects.create(office_id=TbCmuoffices.objects.get(officeid=35),
                                           job_position=request.POST['job_position'],
                                           user=User.objects.get(id=User.objects.latest('id').id))

                return redirect('user_accounts')
            except IntegrityError:
                user = get_user_model()
                users = user.objects.all()
                return render(request, 'cssurvey/useraccounts.html', {'form': UserCreationForm(),
                                                                      'form1': UserChangeForm(),
                                                                      'users': users,
                                                                      'error': 'That username has already been taken.'
                                                                               ' Please choose a new username'})

        else:
            user = get_user_model()
            users = user.objects.all()

            return render(request, 'cssurvey/useraccounts.html', {'form': UserCreationForm(),
                                                                  'form1': UserChangeForm(),
                                                                  'users': users,
                                                                  'error': 'Passwords did not match'})
