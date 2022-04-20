from django.shortcuts import render, redirect, get_object_or_404
from .models import TbQuestions, TbCoverage, TbCmuoffices, TbCssrespondentsDetails, TbEmployees, Ticket
from .forms import TbCssrespondentsForm, TbCssrespondentsDetailsForm, TbCssrespondents, TbQuestionsForm, TbEmployeesForm, UserChangeUpdateForm, UserProfileUpdateForm, TbCmuOfficesForm, TbCmuOfficesAddForm, CreateTicketForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse
from django.core.paginator import Paginator
import datetime


def page_not_found_view(request, exception):
    return render(request, 'cssurvey/error-404.html')


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

                if request.user.groups.all()[0].id == 1:
                    return redirect('controlpanel')
                elif request.user.groups.all()[0].id == 2:
                    return HttpResponse('office admin')
                elif request.user.groups.all()[0].id == 3:
                    return redirect('help_desk')

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
    user_group = request.user.groups.all()[0].id
    if user_group != 1:
        return HttpResponse('BAWAL')
    else:
        return render(request, 'cssurvey/controlpanel.html', {'user_group': user_group})


@login_required
def questions(request):
    user_group = request.user.groups.all()[0].id
    if request.method == 'GET':
        active_questions = TbQuestions.objects.filter(display_status=1)
        inactive_questions = TbQuestions.objects.filter(display_status=0)
        return render(request, 'cssurvey/questions.html', {'active': active_questions,
                                                           'inactive': inactive_questions,
                                                           'searched': '',
                                                           'user_group': user_group})

    else:
        search_data = request.POST
        return_question_data = TbQuestions.objects.filter(survey_question__icontains=search_data.get('searchQuestion'))

        return render(request, 'cssurvey/questions.html', {'active': '',
                                                           'inactive': '',
                                                           'searched': return_question_data,
                                                           'user_group': user_group})


@login_required
def viewquestion(request, question_pk):
    user_group = request.user.groups.all()[0].id
    question = get_object_or_404(TbQuestions, pk=question_pk)
    if request.method == 'GET':
        form = TbQuestionsForm(instance=question)
        return render(request, 'cssurvey/viewquestion.html', {'question': question,
                                                              'form': form,
                                                              'user_group': user_group})
    else:
        try:
            form = TbQuestionsForm(request.POST, instance=question)
            if form.is_valid():
                form.save()
                messages.success(request, 'Changes has been saved successfully.')
                return redirect('viewquestion', question_pk=question_pk)
            else:
                raise ValueError
        except ValueError:
            messages.error(request, 'Bad data passed in. Please try again.')
            return redirect('viewquestion', question_pk=question_pk)


@login_required
def create_question(request):
    user_group = request.user.groups.all()[0].id
    if request.method == 'POST':
        try:
            new_question = TbQuestionsForm(request.POST)
            if new_question.is_valid():
                print(request.POST['survey_question'])
                if request.POST['survey_question'] is None or request.POST['survey_question'] == '':
                    raise ValueError
                else:
                    new_question.save()
                    messages.success(request, 'New question has been created')
                    return redirect('questions')
            else:
                messages.error(request, 'Bad data passed in. Please try again!')
                return redirect('questions')

        except ValueError:
            messages.error(request, 'Bad data passed in. Please try again!')
            return redirect('questions')


@login_required
def delete_question(request, question_pk):
    user_group = request.user.groups.all()[0].id
    del_question = get_object_or_404(TbQuestions, pk=question_pk)
    if request.method == 'POST':
        if del_question.display_status:
            messages.warning(request, 'Cannot perform requested task. The question is still active.')
            return redirect('viewquestion', question_pk=del_question.qid)
        else:
            del_question.delete()
            messages.success(request, 'The survey question has been deleted.')
            return redirect('questions')
    else:
        messages.warning(request, 'Bad request')
        return redirect('questions')


@login_required
def user_accounts(request):
    user_group = request.user.groups.all()[0].id
    form_profile = TbEmployeesForm()
    userid = request.user.id
    if request.method == 'GET':
        user = get_user_model()
        users = user.objects.all()

        return render(request, 'cssurvey/useraccounts.html', {'form': UserCreationForm(),
                                                              'form1': UserChangeForm(),
                                                              'users': users,
                                                              'form_profile': form_profile,
                                                              'userid': userid,
                                                              'user_group': user_group})
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
                messages.success(request, 'New user has been created')
                return redirect('user_accounts')

            except IntegrityError:
                messages.error(request, 'That username has already been taken. Please choose a new username')
                return redirect('user_accounts')

            except ValueError:
                messages.error(request, 'Bad data passed in. Please try again.')
                return redirect('user_accounts')

        else:
            messages.error(request, 'Passwords did not match. Please try again.')
            return redirect('user_accounts')


@login_required
def my_account(request):
    user_group = request.user.groups.all()[0].id
    my_acc = get_object_or_404(User, pk=request.user.id)
    my_det = get_object_or_404(TbEmployees, user=request.user.id)
    form_profile = TbEmployeesForm(instance=my_det)

    user_office = TbEmployees.objects.get(user=request.user.id).office_id
    ticket_open = Ticket.objects.filter(office_id=user_office,
                                        assigned_to=request.user.id,
                                        status=1).count()

    ticket_close = Ticket.objects.filter(office_id=user_office,
                                         assigned_to=request.user.id,
                                         status=3).count()

    ticket_declined = Ticket.objects.filter(office_id=user_office,
                                            assigned_to=request.user.id,
                                            status=2).count()
    if request.method == 'GET':
        return render(request, 'cssurvey/viewuser.html', {'form_profile': form_profile,
                                                          'profile': my_acc,
                                                          'profile_details': my_det,
                                                          'user_group': user_group,
                                                          'own': True,
                                                          'ticket_open': ticket_open,
                                                          'ticket_close': ticket_close,
                                                          'ticket_declined': ticket_declined,})
    else:
        user_form = UserChangeUpdateForm(request.POST, instance=my_acc)
        details_form = UserProfileUpdateForm(request.POST, instance=my_det)

        try:
            if user_form.is_valid() and details_form.is_valid():
                user_form.save()
                details_form.save()
                messages.success(request, 'Changes has been successfully saved!')
                return redirect('my_account')
            else:
                messages.error(request, 'Form did not validate. Please try again')
                return redirect('my_account')
        except ValueError:
            messages.error(request, 'Bad data passed in. Please try again.')
            return redirect('my_account')


@login_required
def my_password(request):
    # change password for user
    user_group = request.user.groups.all()[0].id
    user_details = get_object_or_404(User, username=request.user)
    form = PasswordChangeForm(request.user)
    if request.method == 'GET':
        return render(request, 'cssurvey/changepassword.html', {'profile': user_details,
                                                                'own': True,
                                                                'user_group': user_group,
                                                                'form': form})
    else:
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = form.save(commit=True)
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('my_password')
        else:
            messages.error(request, 'Bad data passed in! Please try again.')
            return redirect('my_password')


@login_required
def view_user(request, user_pk):
    user_group = request.user.groups.all()[0].id
    user_details = get_object_or_404(User, pk=user_pk)
    user_profile = get_object_or_404(TbEmployees, user=user_pk)
    form_profile = TbEmployeesForm(instance=user_profile)
    if request.method == 'GET':
        return render(request, 'cssurvey/viewuser.html', {'form_profile': form_profile,
                                                          'profile': user_details,
                                                          'profile_details': user_profile,
                                                          'user_group': user_group})
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
                messages.success(request, 'Profile update successfully saved')
                return redirect('view_user', user_pk=user_pk)
            else:
                messages.error(request, 'Form did not validate. Please try again')
                return redirect('view_user', user_pk=user_pk)
        except ValueError:
            messages.error(request, 'Bad data passed in. Please try again')
            return redirect('view_user', user_pk=user_pk)


@login_required
def change_password(request, user_pk):
    user_group = request.user.groups.all()[0].id
    user_details = get_object_or_404(User, pk=user_pk)
    if request.method == 'GET':
        return render(request, 'cssurvey/changepassword.html', {'profile': user_details, 'user_group': user_group})
    else:
        try:
            new_password = request.POST['new_password1'].strip()
            confirm_password = request.POST['new_password2'].strip()

            if new_password == '':
                raise ValueError

            if new_password == confirm_password:
                user_details.set_password(new_password)
                user_details.save()
                messages.success(request, 'User\'s password was successfully updated.')
                return redirect('change_password', user_pk=user_pk)
            else:
                messages.error(request, 'Passwords do not match! Please try again.')
                return redirect('change_password', user_pk=user_pk)
        except ValueError:
            messages.error(request, 'Bad data passed in. Please try again.')
            return redirect('change_password', user_pk=user_pk)


@login_required
def deactivate_user(request, user_pk):
    if request.method == 'POST':
        deactivate = get_object_or_404(User, pk=user_pk)
        deactivate.is_active = 0
        deactivate.save()
        messages.info(request, 'The user has been deactivated.')
        return redirect('user_accounts')
    else:
        messages.warning(request, 'Bad request')
        return redirect('user_accounts')


@login_required
def reactivate_user(request, user_pk):
    if request.method == 'POST':
        reactivate = get_object_or_404(User, pk=user_pk)
        reactivate.is_active = 1
        reactivate.save()
        messages.success(request, 'The user has been reactivated.')
        return redirect('user_accounts')
    else:
        messages.warning(request, 'Bad request')
        return redirect('user_accounts')


@login_required
def offices(request):
    user_group = request.user.groups.all()[0].id
    if request.method == 'GET':
        all_offices = TbCmuoffices.objects.all()
        return render(request, 'cssurvey/offices.html', {'offices': all_offices,
                                                         'form': TbCmuOfficesAddForm,
                                                         'user_group': user_group,})
    else:
        try:
            submit_form = TbCmuOfficesAddForm(request.POST)

            if submit_form.is_valid():
                submit_form.save()
                messages.success(request, 'New office has been created')
                return redirect('offices')
            else:
                messages.error(request, 'Form did not validate. Please try again.')
                return redirect('offices')
        except ValueError:
            messages.error(request, 'Bad data passed in. Please try again.')
            return redirect('offices')


@login_required
def view_office(request, office_pk):
    user_group = request.user.groups.all()[0].id
    if request.method == 'GET':
        office = get_object_or_404(TbCmuoffices, pk=office_pk)
        form = TbCmuOfficesForm(instance=office)
        return render(request, 'cssurvey/viewoffice.html', {'office': office,
                                                            'form': form,
                                                            'user_group': user_group,})
    else:
        office = get_object_or_404(TbCmuoffices, pk=office_pk)
        form = TbCmuOfficesForm(instance=office)
        office_form = TbCmuOfficesForm(request.POST, instance=office)
        try:
            if office_form.is_valid():
                office_form.save()
                messages.success(request, 'Changes has been saved successfully')
                return redirect('view_office', office_pk=office.officeid)
            else:
                messages.error(request, 'Form did not validate, please try again.')
                return redirect('view_office', office_pk=office.officeid)
        except ValueError:
            messages.error(request, 'Bad data passed in. Please try again.')
            return redirect('view_office', office_pk=office.officeid)


@login_required
def office_staff(request, office_pk):
    user_group = request.user.groups.all()[0].id
    if request.method == 'GET':
        office = get_object_or_404(TbCmuoffices, pk=office_pk)
        staff = User.objects.filter(tbemployees__office_id=office)
        return render(request, 'cssurvey/officestaff.html', {'office': office,
                                                             'staff': staff,
                                                             'user_group': user_group,})
    else:
        pass


@login_required
def help_desk(request):
    if request.method == 'GET':
        try:
            user_group = request.user.groups.all()[0].id
            user_office = TbEmployees.objects.get(user=request.user.id).office_id

            ticket_open = Ticket.objects.filter(office_id=user_office,
                                                assigned_to=request.user.id,
                                                status=1).count()

            ticket_close = Ticket.objects.filter(office_id=user_office,
                                                 assigned_to=request.user.id,
                                                 status=3).count()

            ticket_declined = Ticket.objects.filter(office_id=user_office,
                                                    assigned_to=request.user.id,
                                                    status=2).count()

            ticket_list = Ticket.objects.filter(office_id=user_office, assigned_to=request.user.id).order_by('-id')
            paginator = Paginator(ticket_list, 5)
            next_ticket_no = Ticket.objects.latest('id').id + 1

            page_number = request.GET.get('page')
            tickets = paginator.get_page(page_number)
            nums = 'a' * tickets.paginator.num_pages
            return render(request, 'cssurvey/helpdesk/helpdesk.html', {'user_group': user_group,
                                                                       'tickets': tickets,
                                                                       'nums': nums,
                                                                       'searched': False,
                                                                       'next_ticket': next_ticket_no,
                                                                       'create_ticket': CreateTicketForm,
                                                                       'user_office': user_office,
                                                                       'ticket_open': ticket_open,
                                                                       'ticket_close': ticket_close,
                                                                       'ticket_declined': ticket_declined,})
        except ValueError:
            messages.error(request, 'Error loading the page. Please try again')
            return redirect('help_desk')
    else:
        user_group = request.user.groups.all()[0].id
        data_searched = request.POST
        user_office = TbEmployees.objects.get(user=request.user.id).office_id
        next_ticket_no = Ticket.objects.latest('id').id + 1

        ticket_open = Ticket.objects.filter(office_id=user_office,
                                            assigned_to=request.user.id,
                                            status=1).count()

        ticket_close = Ticket.objects.filter(office_id=user_office,
                                             assigned_to=request.user.id,
                                             status=3).count()

        ticket_declined = Ticket.objects.filter(office_id=user_office,
                                                assigned_to=request.user.id,
                                                status=2).count()

        return_ticket = Ticket.objects.filter(id__icontains=data_searched.get('search_ticket'),
                                              office_id=user_office,
                                              assigned_to=request.user.id).order_by('-id')
        paginator = Paginator(return_ticket, 5)
        page_number = request.GET.get('page')
        tickets = paginator.get_page(page_number)
        nums = 'a' * tickets.paginator.num_pages
        return render(request, 'cssurvey/helpdesk/helpdesk.html', {'user_group': user_group,
                                                                   'tickets': return_ticket,
                                                                   'nums': nums,
                                                                   'searched': True,
                                                                   'next_ticket': next_ticket_no,
                                                                   'create_ticket': CreateTicketForm,
                                                                   'user_office': user_office,
                                                                   'ticket_open': ticket_open,
                                                                   'ticket_close': ticket_close,
                                                                   'ticket_declined': ticket_declined,})


@login_required
def create_ticket(request):
    if request.method == 'POST':
        try:
            user_office = TbEmployees.objects.get(user=request.user.id).office_id
            next_ticket_no = Ticket.objects.latest('id').id + 1

            new_ticket = CreateTicketForm(request.POST)
            if new_ticket.is_valid():
                ticket = new_ticket.save(commit=False)
                ticket.office_id = user_office
                ticket.ticket_no = next_ticket_no
                ticket.assigned_to = User.objects.get(username=request.user)
                ticket.save()

                messages.success(request, 'New ticket has been submitted')
                return redirect('help_desk')
            else:
                raise ValidationError
        except ValidationError:
            messages.error(request, 'Form did not validate. Please try again.')
            return redirect('help_desk')

        except ValueError:
            messages.error(request, 'Bad data passed in. Please try again.')
            return redirect('help_desk')


@login_required
def view_ticket(request, ticket_id):
    try:
        user_group = request.user.groups.all()[0].id
        user_office = TbEmployees.objects.get(user=request.user.id).office_id
        ticket_open = Ticket.objects.filter(office_id=user_office,
                                            assigned_to=request.user.id,
                                            status=1).count()

        ticket_closed = Ticket.objects.filter(office_id=user_office,
                                              assigned_to=request.user.id,
                                              status=3).count()

        ticket_declined = Ticket.objects.filter(office_id=user_office,
                                                assigned_to=request.user.id,
                                                status=2).count()

        if request.method == 'GET':
            ticket_details = get_object_or_404(Ticket, pk=ticket_id, assigned_to=request.user.id)
            try:
                ticket_details.is_read = 1
                ticket_details.save()
            except ValueError:
                messages.error(request, 'Something went wrong. Please try again')
                return redirect('view_ticket')

            return render(request, 'cssurvey/helpdesk/supportticket.html', {'ticket': ticket_details,
                                                                            'user_group': user_group,
                                                                            'ticket_open': ticket_open,
                                                                            'ticket_close': ticket_closed,
                                                                            'ticket_declined': ticket_declined,})
    except ValueError:
        messages.error(request, 'Something went wrong. Please try again')
        return redirect('view_ticket')


@login_required
def close_ticket(request, ticket_id):
    if request.method == 'POST':
        user_group = request.user.groups.all()[0].id
        user_office = TbEmployees.objects.get(user=request.user.id).office_id

        ticket_close = get_object_or_404(Ticket, pk=ticket_id, assigned_to=request.user.id)
        ticket_close.status = 3
        ticket_close.closed_by = User.objects.get(username=request.user)
        ticket_close.closed_date = datetime.datetime.now()
        ticket_close.save()

        ticket_open = Ticket.objects.filter(office_id=user_office,
                                            assigned_to=request.user.id,
                                            status=1).count()

        ticket_closed = Ticket.objects.filter(office_id=user_office,
                                              assigned_to=request.user.id,
                                              status=3).count()

        ticket_declined = Ticket.objects.filter(office_id=user_office,
                                                assigned_to=request.user.id,
                                                status=2).count()

        return render(request, 'cssurvey/helpdesk/generatelink.html', {'user_group': user_group,
                                                                       'ticket': ticket_close,
                                                                       'ticket_open': ticket_open,
                                                                       'ticket_close': ticket_closed,
                                                                       'ticket_declined': ticket_declined,})
    else:
        messages.error(request, 'Bad request')
        return redirect('help_desk')


@login_required
def decline_ticket(request, ticket_id):
    if request.method == 'POST':
        try:
            ticket_decline = get_object_or_404(Ticket, pk=ticket_id, assigned_to=request.user.id)
            ticket_decline.status = 2
            ticket_decline.closed_by = User.objects.get(username=request.user)
            ticket_decline.closed_date = datetime.datetime.now()
            ticket_decline.save()

            messages.success(request, 'This ticket has been marked as declined')
            return redirect('view_ticket', ticket_id=ticket_id)
        except ValueError:
            messages.error(request, 'Bad data passed in. Please try again.')
            return redirect('help_desk')
    else:
        messages.error(request, 'Bad request')
        return redirect('help_desk')


@login_required
def active_ticket(request):
    if request.method == 'GET':
        try:
            user_group = request.user.groups.all()[0].id
            user_office = TbEmployees.objects.get(user=request.user.id).office_id

            ticket_open = Ticket.objects.filter(office_id=user_office,
                                                assigned_to=request.user.id,
                                                status=1).count()

            ticket_close = Ticket.objects.filter(office_id=user_office,
                                                 assigned_to=request.user.id,
                                                 status=3).count()

            ticket_declined = Ticket.objects.filter(office_id=user_office,
                                                    assigned_to=request.user.id,
                                                    status=2).count()

            ticket_list = Ticket.objects.filter(office_id=user_office,
                                                assigned_to=request.user.id,
                                                status=1).order_by('-id')

            paginator = Paginator(ticket_list, 5)
            next_ticket_no = Ticket.objects.latest('id').id + 1

            page_number = request.GET.get('page')
            tickets = paginator.get_page(page_number)
            nums = 'a' * tickets.paginator.num_pages
            return render(request, 'cssurvey/helpdesk/helpdesk.html', {'user_group': user_group,
                                                                       'tickets': tickets,
                                                                       'nums': nums,
                                                                       'searched': False,
                                                                       'next_ticket': next_ticket_no,
                                                                       'create_ticket': CreateTicketForm,
                                                                       'user_office': user_office,
                                                                       'ticket_open': ticket_open,
                                                                       'ticket_close': ticket_close,
                                                                       'ticket_declined': ticket_declined,})
        except ValueError:
            messages.error(request, 'Error loading the page. Please try again')
            return redirect('help_desk')


@login_required
def closed_ticket(request):
    if request.method == 'GET':
        if request.method == 'GET':
            try:
                user_group = request.user.groups.all()[0].id
                user_office = TbEmployees.objects.get(user=request.user.id).office_id

                ticket_open = Ticket.objects.filter(office_id=user_office,
                                                    assigned_to=request.user.id,
                                                    status=1).count()

                ticket_close = Ticket.objects.filter(office_id=user_office,
                                                     assigned_to=request.user.id,
                                                     status=3).count()

                ticket_declined = Ticket.objects.filter(office_id=user_office,
                                                        assigned_to=request.user.id,
                                                        status=2).count()

                ticket_list = Ticket.objects.filter(office_id=user_office,
                                                    assigned_to=request.user.id,
                                                    status=3).order_by('-id')

                paginator = Paginator(ticket_list, 5)
                next_ticket_no = Ticket.objects.latest('id').id + 1

                page_number = request.GET.get('page')
                tickets = paginator.get_page(page_number)
                nums = 'a' * tickets.paginator.num_pages
                return render(request, 'cssurvey/helpdesk/helpdesk.html', {'user_group': user_group,
                                                                           'tickets': tickets,
                                                                           'nums': nums,
                                                                           'searched': False,
                                                                           'next_ticket': next_ticket_no,
                                                                           'create_ticket': CreateTicketForm,
                                                                           'user_office': user_office,
                                                                           'ticket_open': ticket_open,
                                                                           'ticket_close': ticket_close,
                                                                           'ticket_declined': ticket_declined, })
            except ValueError:
                messages.error(request, 'Error loading the page. Please try again')
                return redirect('help_desk')


@login_required
def declined_ticket(request):
    if request.method == 'GET':
        if request.method == 'GET':
            try:
                user_group = request.user.groups.all()[0].id
                user_office = TbEmployees.objects.get(user=request.user.id).office_id

                ticket_open = Ticket.objects.filter(office_id=user_office,
                                                    assigned_to=request.user.id,
                                                    status=1).count()

                ticket_close = Ticket.objects.filter(office_id=user_office,
                                                     assigned_to=request.user.id,
                                                     status=3).count()

                ticket_declined = Ticket.objects.filter(office_id=user_office,
                                                        assigned_to=request.user.id,
                                                        status=2).count()

                ticket_list = Ticket.objects.filter(office_id=user_office,
                                                    assigned_to=request.user.id,
                                                    status=2).order_by('-id')

                paginator = Paginator(ticket_list, 5)
                next_ticket_no = Ticket.objects.latest('id').id + 1

                page_number = request.GET.get('page')
                tickets = paginator.get_page(page_number)
                nums = 'a' * tickets.paginator.num_pages
                return render(request, 'cssurvey/helpdesk/helpdesk.html', {'user_group': user_group,
                                                                           'tickets': tickets,
                                                                           'nums': nums,
                                                                           'searched': False,
                                                                           'next_ticket': next_ticket_no,
                                                                           'create_ticket': CreateTicketForm,
                                                                           'user_office': user_office,
                                                                           'ticket_open': ticket_open,
                                                                           'ticket_close': ticket_close,
                                                                           'ticket_declined': ticket_declined, })
            except ValueError:
                messages.error(request, 'Error loading the page. Please try again')
                return redirect('help_desk')
