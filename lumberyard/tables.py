# tutorial/tables.py
import django_tables2 as tables
import itertools
from lumberyard.models import Jobs, Sequence, Renders
from django_tables2.utils import A

class JobsTable(tables.Table):
    job_name = tables.TemplateColumn('<a href="jobDetail/{{record.id}}">{{ record.job_name }}</a>')
    job_active = tables.TemplateColumn(
        '<input type="checkbox" id="jobstatus" {% if record.job_active != False %}checked{% endif %} disabled></input>')
    class Meta:
        model = Jobs
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
        exclude = [
            'id',
            'job_dir',
            'milestones',
            'agency_prod_email',
            'agency_prod_phone',
            'client_contact_name',
            'client_contact_email',
            'client_contact_phone',
            'date_pitch',
        ]
        order_by = 'job_name'
    
    """
    'job_active',
    'job_num',
    'job_name',
    'job_dir',
    'date_awarded',
    'email_alias',
    'producer',
    'agency',
    'agency_prod',
    'agency_prod_email',
    'agency_prod_phone',
    'client',
    'client_contact_name',
    'client_contact_email',
    'client_contact_phone',
    'lead_2D',
    'lead_3D',
    'milestones',
    'date_pitch',
    'date_delivery',
    'delivery_specs',
    'artist_list',
    """

class SequenceTable(tables.Table):
    sequence_num = tables.TemplateColumn('<a href="sequenceDetail/{{record.id}}">{{ record.sequence_num }}</a>')
    tasks = tables.Column()
    def render_tasks(self, value):
        if value is not None:
            return ', '.join([tasks.taskType for tasks in value.all()])
        return 'no task'

    class Meta:
        model = Sequence
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
        exclude = [
            'id',
            'job',
        ]
        fields = ("sequence_name", "sequence_num", "sequence_length", "tasks", "due_date", "notes")
        order_by = 'sequence_num'

    """
    'sequence_num',
    'sequence_length',
    'due_date',
    'job_id',
    'sequence_name',
    'notes',
    """

class RendersTable(tables.Table):
    class Meta:
        model = Renders
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
        exclude = [
            'id',
            'shot_name'
        ]
        order_by = 'render_name'

    """
    'render_name',
    'render_timeStamp',
    'render_artist',
    'render_path',
    'render_notes',
    """