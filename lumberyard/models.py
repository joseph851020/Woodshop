from __future__ import unicode_literals
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from djchoices import DjangoChoices, ChoiceItem


def date_plus_30():
    thisValue = datetime.date.today()+datetime.timedelta(days=30)
    return thisValue

class Person(models.Model):
    name = models.CharField(max_length=200,verbose_name="full name")

    def __str__(self):
        return self.name

class Jobs(models.Model):
    class Meta:
        verbose_name = 'Jobs'
        verbose_name_plural = 'Jobs'

    job_name = models.CharField(max_length=200)
    job_active = models.BooleanField(default=True)
    job_num = models.CharField(max_length=200)
    job_dir = models.CharField(max_length=200, default='NONE', editable=False)
    email_alias = models.EmailField(default='none@woodshop.tv')
    producer = models.ForeignKey('Employee', related_name='job_producer')
    lead_2D = models.ForeignKey('Employee', related_name = 'job_lead_2D')
    lead_3D = models.ForeignKey('Employee', related_name = 'job_lead_3D')
    agency = models.CharField(max_length=200, default='NONE')
    agency_prod = models.CharField(max_length=200, default='NONE')
    agency_prod_email = models.CharField(max_length=200, default='NONE')
    agency_prod_phone = models.CharField(max_length=200, default='NONE')
    client = models.CharField(max_length=200, default='NONE')
    client_contact_name = models.CharField(max_length=200, default='NONE')
    client_contact_email = models.CharField(max_length=200, default='NONE')
    client_contact_phone = models.CharField(max_length=200, default='NONE')
    milestones = models.CharField(max_length=200, default='NONE')
    date_awarded = models.DateField(default=datetime.date.today, blank=True)
    date_pitch = models.DateField(default=datetime.date.today, blank=True)
    date_delivery = models.DateField('date delivery', default=date_plus_30)
    delivery_specs = models.ForeignKey('DeliverySpecs')
    artist_list = models.ManyToManyField('Employee')

    def __str__(self):
        return self.job_name

class DeliverySpecs(models.Model):

    class Meta:
        verbose_name = 'DeliverySpecs'
        verbose_name_plural = 'DeliverySpecs'
    spec_name = models.CharField(max_length=200, default='1080p Prorez QT')
    spec_rez = models.CharField(max_length=50, default='1920x1080')
    spec_format = models.CharField(max_length=50, default='Quicktime')

    def __str__(self):
        return self.spec_name

class Departments(models.Model):
    
    class Meta:
        verbose_name = 'Departments'
        verbose_name_plural = 'Departments'

    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name    

class Tasks(models.Model):

    class Meta:
        verbose_name = 'Tasks'
        verbose_name_plural = 'Tasks'

    class TaskType(DjangoChoices):
        animation = ChoiceItem('ANIMATION')
        colorAndLighting = ChoiceItem('COLOR & LIGHTING')
        tracking = ChoiceItem('TRACKIGN')
        dynamics = ChoiceItem('DYNAMICS')
        texture = ChoiceItem('TEXTURE')
        comp = ChoiceItem('COMP')
        modeling = ChoiceItem('MODELING')
        design = ChoiceItem('DESIGN')

    taskType = models.CharField(max_length=20,
                            choices=TaskType.choices,
                            validators=[TaskType.validator],
                            default='ANIMATION')

    def __str__(self):
        return self.taskType

class Employee(models.Model):
    class EmployeeType(DjangoChoices):
        Staff = ChoiceItem('S')
        Freelance = ChoiceItem('F')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employeeType = models.CharField(max_length=1,
                            choices=EmployeeType.choices,
                            validators=[EmployeeType.validator])
    department = models.ForeignKey('Departments',on_delete=models.CASCADE)
    rate = models.CharField(max_length=200, default='NONE')
    phone = models.CharField(max_length=200, default='NONE')
    url = models.CharField(max_length=200, default='NONE')
    notes = models.TextField(max_length=200, default='NONE')

    def __str__(self):
        return self.user.get_full_name()


class Sequence(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    sequence_name = models.CharField(max_length=100)    
    sequence_num = models.CharField(max_length=10)
    sequence_length = models.IntegerField(default=0)
    tasks = models.ManyToManyField('Tasks')
    due_date = models.DateTimeField('due date')
    notes = models.TextField(max_length=200, default='NONE')

    def __str__(self):
        return self.sequence_name

class Renders(models.Model):
    class Meta:
        verbose_name = 'Renders'
        verbose_name_plural = 'Renders'

    shot_name = models.ForeignKey(Sequence, on_delete=models.CASCADE)
    render_name = models.CharField(max_length=100)
    render_timeStamp = models.DateTimeField(default=datetime.datetime.today, blank=True)
    render_artist = models.CharField(max_length=100)
    render_path = models.CharField(max_length=100)
    render_notes = models.TextField()

    def __str__(self):
        return self.render_name

