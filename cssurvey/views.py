from django.shortcuts import render, redirect
from .models import Question
from .forms import CustomerFeedbackForm
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
    questions = Question.objects.all()
    if request.method == 'GET':
        return render(request, 'cssurvey/customersurvey.html', {'questions': questions, 'form': CustomerFeedbackForm})
    else:
        try:
            form = CustomerFeedbackForm(request.POST)
            newcss = form.save(commit=False)

            rates = [newcss.rate1, newcss.rate2, newcss.rate3, newcss.rate4, newcss.rate5, ]
            for rate in rates:
                if int(rate) > 5:
                    raise ValueError

            newcss.rate1 = request.POST.get('rate1')
            newcss.rate2 = request.POST.get('rate2')
            newcss.rate3 = request.POST.get('rate3')
            newcss.rate4 = request.POST.get('rate4')
            newcss.rate5 = request.POST.get('rate5')
            newcss.save()
            return redirect('submitcss')
        except ValueError:
            return render(
                request,
                'cssurvey/customersurvey.html',
                {'questions': questions, 'form': CustomerFeedbackForm, 'error': 'Bad data passed in. Please try again!'}
            )


def submitcss(request):
    return render(request, 'cssurvey/submitcss.html')


@login_required
def controlpanel(request):
    return render(request, 'cssurvey/controlpanel.html')
