from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from . models import Applicant, Document
from . models import Resume, company_profile


class ApplicantCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Applicant
        fields = ('username', 'email', 'phone','password1','password2')


class ApplicantChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = Applicant
        fields = ('email', 'password')


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)


class cv_builderCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Resume
        fields = ('__all__')


class CompanyForm(forms.ModelForm):
    class Meta:
        model = company_profile
        fields = ('company_address', 'city', 'company_contact', 'company_tag_name', 'company_bio', 'profile_picture', 'number_of_employee', 'company_name')



class CompanyCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Applicant
        fields = ('username', 'email','password1','password2','is_company')