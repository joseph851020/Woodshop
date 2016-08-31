from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.views.generic import FormView
from lumberyard.forms import LoginForm, JobDetailForm
from lumberyard.models import Jobs, Sequence, Renders
from lumberyard.tables import JobsTable, SequenceTable, RendersTable
from django_tables2 import RequestConfig
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.db.models import Q
import time

@login_required(login_url='/')
def indexView(request):
    results = Jobs.objects.filter(Q(job_active = 1))
    table = JobsTable(results)
    RequestConfig(request, paginate={'per_page': 12}).configure(table)
    return render(request, 'lumberyard/index.html', {'table': table})


class LoginView(generic.FormView):
    form_class = LoginForm
    success_url = reverse_lazy('lumberyard:index')
    template_name = 'lumberyard/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)

def JobDetailView(request, job_id):
    job_name = Jobs.objects.get( id = job_id ).job_name
    job_num = Jobs.objects.get( id = job_id ).job_num
    producer = Jobs.objects.get( id = job_id ).producer
    email_alias = Jobs.objects.get( id= job_id ).email_alias
    lead_2D = Jobs.objects.get( id= job_id ).lead_2D
    lead_3D = Jobs.objects.get( id= job_id ).lead_3D
    date_awarded = Jobs.objects.get( id= job_id ).date_awarded
    date_pitch = Jobs.objects.get( id= job_id ).date_pitch
    date_delivery = Jobs.objects.get( id= job_id ).date_delivery
    agency = Jobs.objects.get( id= job_id ).agency
    agency_prod = Jobs.objects.get( id= job_id ).agency_prod
    agency_prod_email = Jobs.objects.get( id= job_id ).agency_prod_email
    agency_prod_phone = Jobs.objects.get( id= job_id ).agency_prod_phone
    client = Jobs.objects.get( id= job_id ).client
    client_contact_name = Jobs.objects.get( id= job_id ).client_contact_name
    client_contact_email = Jobs.objects.get( id= job_id ).client_contact_email
    client_contact_phone = Jobs.objects.get( id= job_id ).client_contact_phone
    results = Sequence.objects.filter(Q(job__job_name = job_name))
    table = SequenceTable(results)
    RequestConfig(request, paginate={'per_page': 12}).configure(table)
    return render(request, 'lumberyard/jobDetail.html', {
        'job_name': job_name,
        'job_num': job_num,
        'producer': producer,
        'email_alias': email_alias,
        'lead_2D': lead_2D,
        'lead_3D': lead_3D,
        'date_awarded': date_awarded,
        'date_pitch': date_pitch,
        'date_delivery': date_delivery,
        'agency': agency,
        'agency_prod': agency_prod,
        'agency_prod_email': agency_prod_email,
        'agency_prod_phone': agency_prod_phone,
        'client': client,
        'client_contact_name': client_contact_name,
        'client_contact_email': client_contact_email,
        'client_contact_phone': client_contact_phone,
        'table': table,
    })

def sequenceDetailView(request, job_id, sequence_id):
    job_name = Jobs.objects.get( id = job_id ).job_name
    job_num = Jobs.objects.get( id = job_id ).job_num
    sequence_name = Sequence.objects.get( id = sequence_id ).sequence_name
    artist_list = Jobs.objects.get( id = job_id ).artist_list.all()
    tasks = Sequence.objects.get ( id = sequence_id ).tasks.all()
    producer = Jobs.objects.get( id = job_id ).producer
    email_alias = Jobs.objects.get( id= job_id ).email_alias
    lead_2D = Jobs.objects.get( id= job_id ).lead_2D
    lead_3D = Jobs.objects.get( id= job_id ).lead_3D
    date_awarded = Jobs.objects.get( id= job_id ).date_awarded
    date_pitch = Jobs.objects.get( id= job_id ).date_pitch
    date_delivery = Jobs.objects.get( id= job_id ).date_delivery
    results = Renders.objects.filter(
        Q(shot_name__id = sequence_id ) &
        Q(shot_name__job_id = job_id)
    )
    table = RendersTable(results)
    RequestConfig(request, paginate={'per_page': 12}).configure(table)
    return render(request, 'lumberyard/sequenceDetail.html', {
        'job_id': job_id,
        'job_name': job_name,
        'job_num': job_num,
        'sequence_name': sequence_name,
        'artist_list': artist_list,
        'tasks': tasks,
        'producer': producer,
        'email_alias': email_alias,
        'lead_2D': lead_2D,
        'lead_3D': lead_3D,
        'date_awarded': date_awarded,
        'date_pitch': date_pitch,
        'date_delivery': date_delivery,
        'table': table,
    })

def ajaxjobsearch(request):

    if request.is_ajax():
        startdate = request.GET.get('startdate')
        enddate = request.GET.get('enddate')
        datetype = request.GET.get('datetype')
        jobstatus = request.GET.get('jobstatus')
        searchtext = request.GET.get('searchtext')
        if jobstatus != '2':
            if datetype == "date_awarded":
                if startdate != '' and enddate != '':
                    results = Jobs.objects.filter(
                        Q( job_active = jobstatus ) &
                        Q( date_awarded__range = [startdate, enddate] ) &
                        (Q( job_name__contains = searchtext ) |
                        Q( job_num__contains = searchtext ) |
                        Q( email_alias__contains = searchtext ) |
                        Q( producer__user__first_name__contains = searchtext ) |
                        Q( producer__user__last_name__contains = searchtext ) |
                        Q( lead_2D__user__first_name__contains = searchtext ) |
                        Q( lead_2D__user__last_name__contains = searchtext ) |
                        Q( lead_3D__user__first_name__contains = searchtext ) |
                        Q( lead_3D__user__last_name__contains = searchtext ) |
                        Q( agency__contains = searchtext ) |
                        Q( agency_prod__contains = searchtext ) |
                        Q( delivery_specs__spec_name__contains = searchtext ) |
                        Q( client__contains = searchtext ))
                    ).order_by( 'job_name' )
                    table = JobsTable(results)
                    RequestConfig(request, paginate={'per_page': 12}).configure(table)
                    return render(request, 'lumberyard/jobsTable.html', {'table': table})
                else:
                    results = Jobs.objects.filter(
                        Q( job_active = jobstatus ) &
                        (Q( job_name__contains = searchtext ) |
                        Q( job_num__contains = searchtext ) |
                        Q( email_alias__contains = searchtext ) |
                        Q( producer__user__first_name__contains = searchtext ) |
                        Q( producer__user__last_name__contains = searchtext ) |
                        Q( lead_2D__user__first_name__contains = searchtext ) |
                        Q( lead_2D__user__last_name__contains = searchtext ) |
                        Q( lead_3D__user__first_name__contains = searchtext ) |
                        Q( lead_3D__user__last_name__contains = searchtext ) |
                        Q( agency__contains = searchtext ) |
                        Q( agency_prod__contains = searchtext ) |
                        Q( delivery_specs__spec_name__contains = searchtext ) |
                        Q( client__contains = searchtext ))
                    ).order_by( 'job_name' )
                    table = JobsTable(results)
                    RequestConfig(request, paginate={'per_page': 12}).configure(table)
                    return render(request, 'lumberyard/jobsTable.html', {'table': table})

            else:
                if startdate != '' and enddate != '':
                    results = Jobs.objects.filter(
                        Q( job_active = jobstatus ) &
                        Q( date_delivery__range = [startdate, enddate] ) &
                        (Q( job_name__contains = searchtext ) |
                        Q( job_num__contains = searchtext ) |
                        Q( email_alias__contains = searchtext ) |
                        Q( producer__user__first_name__contains = searchtext ) |
                        Q( producer__user__last_name__contains = searchtext ) |
                        Q( lead_2D__user__first_name__contains = searchtext ) |
                        Q( lead_2D__user__last_name__contains = searchtext ) |
                        Q( lead_3D__user__first_name__contains = searchtext ) |
                        Q( lead_3D__user__last_name__contains = searchtext ) |
                        Q( agency__contains = searchtext ) |
                        Q( agency_prod__contains = searchtext ) |
                        Q( delivery_specs__spec_name__contains = searchtext ) |
                        Q( client__contains = searchtext ))
                    ).order_by( 'job_name' )
                    table = JobsTable(results)
                    RequestConfig(request, paginate={'per_page': 12}).configure(table)
                    return render(request, 'lumberyard/jobsTable.html', {'table': table})
                else:
                    results = Jobs.objects.filter(
                        Q( job_active = jobstatus ) &
                        (Q( job_name__contains = searchtext ) |
                        Q( job_num__contains = searchtext ) |
                        Q( email_alias__contains = searchtext ) |
                        Q( producer__user__first_name__contains = searchtext ) |
                        Q( producer__user__last_name__contains = searchtext ) |
                        Q( lead_2D__user__first_name__contains = searchtext ) |
                        Q( lead_2D__user__last_name__contains = searchtext ) |
                        Q( lead_3D__user__first_name__contains = searchtext ) |
                        Q( lead_3D__user__last_name__contains = searchtext ) |
                        Q( agency__contains = searchtext ) |
                        Q( agency_prod__contains = searchtext ) |
                        Q( delivery_specs__spec_name__contains = searchtext ) |
                        Q( client__contains = searchtext ))
                    ).order_by( 'job_name' )
                    table = JobsTable(results)
                    RequestConfig(request, paginate={'per_page': 12}).configure(table)
                    return render(request, 'lumberyard/jobsTable.html', {'table': table})

        else:
            if datetype == "date_awarded":
                if startdate != '' and enddate != '':
                    results = Jobs.objects.filter(
                        Q( date_awarded__range = [startdate, enddate] ) &
                        (Q( job_name__contains = searchtext ) |
                        Q( job_num__contains = searchtext ) |
                        Q( email_alias__contains = searchtext ) |
                        Q( producer__user__first_name__contains = searchtext ) |
                        Q( producer__user__last_name__contains = searchtext ) |
                        Q( lead_2D__user__first_name__contains = searchtext ) |
                        Q( lead_2D__user__last_name__contains = searchtext ) |
                        Q( lead_3D__user__first_name__contains = searchtext ) |
                        Q( lead_3D__user__last_name__contains = searchtext ) |
                        Q( agency__contains = searchtext ) |
                        Q( agency_prod__contains = searchtext ) |
                        Q( delivery_specs__spec_name__contains = searchtext ) |
                        Q( client__contains = searchtext ))
                    ).order_by( 'job_name' )
                    table = JobsTable(results)
                    RequestConfig(request, paginate={'per_page': 12}).configure(table)
                    return render(request, 'lumberyard/jobsTable.html', {'table': table})
                else:
                    results = Jobs.objects.filter(
                        Q( job_name__contains = searchtext ) |
                        Q( job_num__contains = searchtext ) |
                        Q( email_alias__contains = searchtext ) |
                        Q( producer__user__first_name__contains = searchtext ) |
                        Q( producer__user__last_name__contains = searchtext ) |
                        Q( lead_2D__user__first_name__contains = searchtext ) |
                        Q( lead_2D__user__last_name__contains = searchtext ) |
                        Q( lead_3D__user__first_name__contains = searchtext ) |
                        Q( lead_3D__user__last_name__contains = searchtext ) |
                        Q( agency__contains = searchtext ) |
                        Q( agency_prod__contains = searchtext ) |
                        Q( delivery_specs__spec_name__contains = searchtext ) |
                        Q( client__contains = searchtext )
                    ).order_by( 'job_name' )
                    table = JobsTable(results)
                    RequestConfig(request, paginate={'per_page': 12}).configure(table)
                    return render(request, 'lumberyard/jobsTable.html', {'table': table})

            else:
                results = Jobs.objects.filter(
                    Q( date_delivery__range = [startdate, enddate] ) &
                    (Q( job_name__contains = searchtext ) |
                     Q( job_num__contains = searchtext ) |
                     Q( email_alias__contains = searchtext ) |
                     Q( producer__user__first_name__contains = searchtext ) |
                     Q( producer__user__last_name__contains = searchtext ) |
                     Q( lead_2D__user__first_name__contains = searchtext ) |
                     Q( lead_2D__user__last_name__contains = searchtext ) |
                     Q( lead_3D__user__first_name__contains = searchtext ) |
                     Q( lead_3D__user__last_name__contains = searchtext ) |
                     Q( agency__contains = searchtext ) |
                     Q( agency_prod__contains = searchtext ) |
                     Q( delivery_specs__spec_name__contains = searchtext ) |
                     Q( client__contains = searchtext ))
                ).order_by( 'job_name' )
                if startdate != '' and enddate != '':
                    table = JobsTable(results)
                    RequestConfig(request, paginate={'per_page': 12}).configure(table)
                    return render(request, 'lumberyard/jobsTable.html', {'table': table})
                else:
                    results = Jobs.objects.filter(
                        Q( job_name__contains = searchtext ) |
                        Q( job_num__contains = searchtext ) |
                        Q( email_alias__contains = searchtext ) |
                        Q( producer__user__first_name__contains = searchtext ) |
                        Q( producer__user__last_name__contains = searchtext ) |
                        Q( lead_2D__user__first_name__contains = searchtext ) |
                        Q( lead_2D__user__last_name__contains = searchtext ) |
                        Q( lead_3D__user__first_name__contains = searchtext ) |
                        Q( lead_3D__user__last_name__contains = searchtext ) |
                        Q( agency__contains = searchtext ) |
                        Q( agency_prod__contains = searchtext ) |
                        Q( delivery_specs__spec_name__contains = searchtext ) |
                        Q( client__contains = searchtext )
                    ).order_by( 'job_name' )
                    table = JobsTable(results)
                    RequestConfig(request, paginate={'per_page': 12}).configure(table)
                    return render(request, 'lumberyard/jobsTable.html', {'table': table})

def ajaxsequencesearch(request):

    if request.is_ajax():
        sequencenum1 = request.GET.get('sequencenum1')
        sequencenum2 = request.GET.get('sequencenum2')
        searchtext = request.GET.get('searchtext')
        jobname = request.GET.get('jobname')
        if sequencenum1 != '' and sequencenum2 != '':
            results = Sequence.objects.filter(
                Q( job__job_name = jobname) &
                Q( sequence_num__range = [sequencenum1, sequencenum2] ) &
                (Q( sequence_name__contains = searchtext ) |
                Q( tasks__taskType__contains = searchtext ) |
                Q( notes__contains = searchtext ) )
            ).distinct( ).order_by( 'sequence_name' )
            table = SequenceTable(results)
            RequestConfig(request, paginate={'per_page': 12}).configure(table)
            return render(request, 'lumberyard/jobsTable.html', {'table': table})
        else:
            results = Sequence.objects.filter(
                Q( job__job_name = jobname) &
                (Q( sequence_name__contains = searchtext ) |
                Q( tasks__taskType__contains = searchtext ) |
                Q( notes__contains = searchtext ))
            ).distinct( ).order_by( 'sequence_name' )
            table = SequenceTable(results)
            RequestConfig(request, paginate={'per_page': 12}).configure(table)
            return render(request, 'lumberyard/jobsTable.html', {'table': table})

def ajaxrendersearch(request):

    if request.is_ajax():
        searchtext = request.GET.get('searchtext')
        jobname = request.GET.get('jobname')
        sequencename = request.GET.get('sequencename')
        results = Renders.objects.filter(
            Q( shot_name__job__job_name = jobname) &
            Q( shot_name__sequence_name = sequencename ) &
            (Q( render_name__contains = searchtext ) |
            Q( render_artist__contains = searchtext ) |
            Q( render_path__contains = searchtext ) |
            Q( render_notes__contains = searchtext ))
        ).distinct( ).order_by( 'render_name' )
        table = RendersTable(results)
        RequestConfig(request, paginate={'per_page': 12}).configure(table)
        return render(request, 'lumberyard/jobsTable.html', {'table': table})

def jobsEditView():
    pass


"""
class JobsModelAdmin(admin.ModelAdmin):
    def get_form(self.request, obj=None, **kwargs):
        if request.user.is_superuser:
            kwargs['form'] = MySuperuserForm

        return super(MyModelAdmin, self).get_form(request, obj, **kwargs)
"""

