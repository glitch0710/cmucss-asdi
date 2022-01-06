from django.shortcuts import render, redirect
from .models import Question
from .forms import CustomerFeedbackForm


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
            return render(request, 'cssurvey/customersurvey.html', {'questions': questions,
                                                                    'form': CustomerFeedbackForm,
                                                                    'error': 'Bad data passed in. Please try again!'})


def submitcss(request):
    return render(request, 'cssurvey/submitcss.html')


def controlpanel(request):
    return render(request, 'cssurvey/controlpanel.html')
