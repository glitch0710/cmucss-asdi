from django.shortcuts import render


def index(request):
    return render(request, 'cssurvey/index.html')

def customersurvey(request):
    return render(request, 'cssurvey/customersurvey.html')
