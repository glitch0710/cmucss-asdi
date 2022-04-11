"""css URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from cssurvey import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Auth
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),

    # CSS
    path('', views.index, name='home'),
    path('css/', views.customersurvey, name='customersurvey'),
    path('css/submitcss', views.submitcss, name='submitcss'),
    path('cpanel/', views.controlpanel, name='controlpanel'),
    path('cpanel/surveyquestions/', views.questions, name='questions'),
    path('cpanel/surveyquestions/create', views.create_question, name='create_question'),
    path('cpanel/surveyquestions/<int:question_pk>', views.viewquestion, name='viewquestion'),
    path('cpanel/surveyquestions/<int:question_pk>/delete', views.delete_question, name='delete_question'),
    path('cpanel/users', views.user_accounts, name='user_accounts'),
    path('cpanel/users/<int:user_pk>', views.view_user, name='view_user'),
    path('cpanel/users/<int:user_pk>/security', views.change_password, name='change_password'),
    path('cpanel/users/<int:user_pk>/deactivate', views.deactivate_user, name='deactivate_user'),
    path('cpanel/users/<int:user_pk>/reactivate', views.reactivate_user, name='reactivate_user'),
    path('cpanel/offices', views.offices, name='offices'),
    path('cpanel/offices/<int:office_pk>', views.view_office, name='view_office'),
    path('cpanel/offices/<int:office_pk>/staff', views.office_staff, name='office_staff'),
    path('helpdesk/', views.help_desk, name='help_desk'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'cssurvey.views.page_not_found_view'

