from django.shortcuts import render, redirect, get_object_or_404
from .models import TbQuestions, TbCoverage, TbCmuoffices, TbCssrespondentsDetails
from .forms import TbCssrespondentsForm, TbCssrespondentsDetailsForm, TbCssrespondents, TbQuestionsForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


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
