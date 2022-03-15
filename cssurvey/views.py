from django.shortcuts import render, redirect
from .models import TbQuestions, TbCoverage, TbCmuoffices
from .forms import TbCssrespondentsForm, TbCssrespondentsDetailsForm, TbCssrespondents
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
    questions = TbQuestions.objects.all()
    if request.method == 'GET':
        return render(request, 'cssurvey/customersurvey.html', {'questions': questions,
                                                                'form': TbCssrespondentsForm,
                                                                'form1': TbCssrespondentsDetailsForm})
    else:
        # try:
            form = TbCssrespondentsForm(request.POST)
            newcss = form.save(commit=False)

            newcss.employee_id = 0
            newcss.coverageid = TbCoverage.objects.get(coverageid=5)
            newcss.respondedofficeid = TbCmuoffices.objects.get(officeid=35)

            newcss.save()

            last_id = TbCssrespondents.objects.latest('respondentid')

            newcssdetails = form.save(commit=False)

            for question in questions:
                newcssdetails.respondentid = last_id
                newcssdetails.qid = question.QID
                newcssdetails.rating = 'rate' + question.QID
                newcssdetails.save()

            # rates = [newcss.rate1, newcss.rate2, newcss.rate3, newcss.rate4, newcss.rate5, ]
            #
            # for rate in rates:
            #     if int(rate) > 5:
            #         raise ValueError
            #
            # for question in questions:
            #     newcss1.qid = question.QID
            #     newcss1.rating = request.POST.get('rate' + question.QID)
            #
            # newcss1.save()
            # newcss.save()
            return redirect('submitcss')
        # except ValueError:
        #     return render(
        #         request,
        #         'cssurvey/customersurvey.html',
        #         {'questions': questions, 'form': TbCssrespondentsForm, 'error': 'Bad data passed in. Please try again!'}
        #     )


def submitcss(request):
    return render(request, 'cssurvey/submitcss.html')


@login_required
def controlpanel(request):
    return render(request, 'cssurvey/controlpanel.html')
