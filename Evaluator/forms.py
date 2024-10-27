import datetime

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django.utils.translation import gettext as _

from . import models

def present_or_future_date(value):
    """
    This function is to be used with validator argument for a form field.
    It checks if date entered by user is either present day or a future date.
    """
    if value < datetime.date.today():
        raise forms.ValidationError("The date cannot be in the past!")
    return value


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2' )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False) # Don't save it yet
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class CreateJobOpeningForm(forms.ModelForm):
    disabled_fields = ['position']

    class Meta:
        model = models.JobOpening
        fields = ('position', 'no_of_openings')

    def __init__(self, *args, **kwargs):
        super(CreateJobOpeningForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for field in self.disabled_fields:
                self.fields[field].disabled = True


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False) # Don't save it yet
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class AnswerForm(forms.ModelForm):
    class Meta:
        models = models.Answer
        fields = ['detail', 'correct']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['description', 'difficulty', 'skill', 'qset']

AnswerFormSet = forms.modelformset_factory(models.Answer, form=AnswerForm, extra=2)

AnswerInLineFormSet = forms.inlineformset_factory(
        models.Question,
        models.Answer,
        extra=1,
        fields=('detail', 'correct'),
        formset=AnswerFormSet,
        min_num=1,
        )

class AddCandidateForm(forms.ModelForm):
    class Meta:
        model = models.Candidate
        fields = ['name', 'experience', 'position_applied', 'contact_primary', 'vendor', 'skill']
        labels = {
        "contact_primary": _("Contact No:"),

        }

class QuestionSetForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    class Meta:
        model = models.QuestionSet
        fields = ['name',]

class AddInterview(forms.ModelForm):
    disabled_fields = ('candidate', 'position', 'date')
    class Meta:
        model = models.Interview
        fields = ['candidate', 'position', 'date' , 'question_set']

    def __init__(self, *args, **kwargs):
        super(AddInterview, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for field in self.disabled_fields:
                self.fields[field].disabled = True

    date = forms.DateField(widget=AdminDateWidget()) # This shows the admin calender on the frontend form


class RoundForm(forms.ModelForm):
    class Meta:
        models = models.Round
        fields = ['name', 'date', 'contact_time', 'assignee', 'supporting_interviewer', 'round_type', 'result', 'comments']


    date = forms.DateField(widget=AdminDateWidget(), validators=[present_or_future_date])

RoundFormSet = forms.modelformset_factory(
        models.Round,
        form=RoundForm,
        extra=0,
        )

RoundInLineFormSet = forms.inlineformset_factory(
        models.Interview,
        models.Round,
        extra=0,
        fields=('name', 'date', 'contact_time', 'assignee', 'supporting_interviewer', 'round_type', 'result', 'comments'),
        formset=RoundFormSet,
        min_num=0,
        )

class BulkCreateInterviewsAndCandidates(forms.Form):
    name_list = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'required': True}),
        help_text='Please mention names in separate lines',
        label='Candidate List',
        )
    position = forms.ModelChoiceField(
        queryset=models.Position.objects.all(),
        widget=forms.Select(attrs={'class':'form-control my-4', 'required': True}),
        label='Position *',
        )
    experience = forms.IntegerField(label='Exp *',)
    date = forms.DateField(widget=AdminDateWidget(attrs={'required': True}))

    vendor = forms.ModelChoiceField(
        queryset=models.Vendor.objects.all(),
        widget=forms.Select(attrs={'class':'form-control mt-4', 'required': True}),
        label='Vendor *',

        )

class DocumentForm(forms.ModelForm):
    class Meta:
        model = models.Document
        fields = ('document', )
