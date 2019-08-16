from django import forms
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Fieldset, ButtonHolder
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)


class LoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            ButtonHolder(
                Submit('login','login', css_class='btn-primary')
            )
        )

class JobDetailForm(forms.Form):
    job_active = forms.BooleanField(label='Job Active')
    job_num = forms.CharField(label='Job Number',max_length=10)
    job_name = forms.CharField(label='Job Name',max_length=100)
    job_dir = forms.CharField(label='Job Folder',max_length=200)
    date_pitch = forms.DateField(label='Date Pitched')
    date_awarded = forms.DateField(label='Date Awarded',required=False)
    date_delivery = forms.DateField(label='Date of Delivery')
    email_alias = forms.EmailField(label='Email Alias')
    producer = forms.ChoiceField(label='Producer')
    agency = forms.CharField(label='Agency',required=False,max_length=200)
    agency_prod = forms.CharField(label='Agency Producer',required=False,max_length=200)
    agency_prod_email = forms.CharField(label='Agency Email',required=False,max_length=200)
    agency_prod_phone = forms.CharField(label='Agency Phone',required=False,max_length=50)
    client = forms.CharField(label='Client',required=False,max_length=200)
    client_contact_name = forms.CharField(label='Client Contact',required=False,max_length=200)
    client_contact_email = forms.CharField(label='Client Email',required=False,max_length=200)
    client_contact_phone = forms.CharField(label='Client Phone',required=False,max_length=50)
    lead_2D = forms.ChoiceField(label='Lead 2D')
    lead_3D = forms.ChoiceField(label='Lead 3D')
    milestones = forms.CharField(label='Milestones',required=False, max_length=200)
    delivery_specs = forms.ChoiceField(label='Delivery Specs')
    artist_list = forms.MultipleChoiceField(label='Artist List')
    
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.layout = Layout(
        Field('job_active', css_class='input-sm'),
        Field('job_num', css_class='input-sm'),
        Field('job_name', css_class='input-sm'),
        Field('job_dir', css_class='input-sm'),
        Field('date_pitch', css_class='input-sm'),
        Field('date_awarded', css_class='input-sm'),
        Field('date_delivery', css_class='input-sm'),
        Field('email_alias', css_class='input-sm'),
        Field('producer', css_class='input-sm'),
        Field('agency', css_class='input-sm'),
        Field('agency_prod', css_class='input-sm'),
        Field('agency_prod_email', css_class='input-sm'),
        Field('agency_prod_phone', css_class='input-sm'),
        Field('client', css_class='input-sm'),
        Field('client_contact_name', css_class='input-sm'),
        Field('client_contact_email', css_class='input-sm'),
        Field('client_contact_phone', css_class='input-sm'),
        Field('lead_2D', css_class='input-sm'),
        Field('lead_3D', css_class='input-sm'),
        Field('milestones', css_class='input-sm'),
        Field('delivery_specs', css_class='input-sm'),
        Field('artist_list', css_class='input-sm'),
        FormActions(Submit('save', 'save', css_class='btn-primary'))
    )

