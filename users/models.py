from django.db import models
from django.contrib.auth.models import AbstractUser # use AbstractUser which actually subclasses AbstractBaseUser but provides more default configuration.
from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

from .validators import validate_file_extension


class Applicant(AbstractUser):
    phone = models.CharField(max_length=55, blank=True, null=True)
    company_name = models.CharField(max_length=55, blank=True, null=True)
    title = models.CharField(max_length=55, blank=True, null=True)
    position = models.CharField(max_length=55, blank=True, null=True)
    place = models.CharField(max_length=55, blank=True, null=True)
    country = models.CharField(max_length=55, blank=True, null=True)
    business = models.CharField(max_length=55, blank=True, null=True)
    employee = models.CharField(max_length=55, blank=True, null=True)
    street = models.CharField(max_length=55, blank=True, null=True)
    additional = models.CharField(max_length=55, blank=True, null=True)
    zip = models.CharField(max_length=55, blank=True, null=True)
    code = models.CharField(max_length=55, blank=True, null=True )
    is_company = models.BooleanField(default=False)
    location = models.CharField(max_length=100 , null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = "Applicant"


class company_profile(models.Model):
    company_name = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    number_of_employee = models.CharField(max_length=100, null=True, blank=True)
    company_address = models.CharField(max_length=255, null=True, blank=True)
    company_contact = models.CharField(max_length=100, null=True, blank=True)
    company_tag_name = models.CharField(max_length=100, null=True, blank=True)
    company_bio = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.FileField(upload_to='pictures/', null=True, blank=True)
    company = models.ForeignKey(Applicant, on_delete=models.CASCADE, null=True,)

    class Meta:
        db_table = "company_profile"

    class Meta:
        db_table = "company_profile"


class Job_Post(models.Model):
    Job_title = models.CharField(max_length=100)
    job_designation = models.CharField(max_length=255)
    Job_Description = models.CharField(max_length=100)
    qualification_required = models.CharField(max_length=100, null=True, blank=True)
    positions = models.CharField(max_length=100)
    experience_required = models.CharField(max_length=100)
    City = models.CharField(max_length=100 , null=True, blank=True)
    Country = models.CharField(max_length=100)
    complete_address = models.CharField(max_length=100)
    Region = models.CharField(max_length=100)
    gender_preference = models.CharField(max_length=100)
    job_nature = models.CharField(max_length=100)
    #avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    status = models.BooleanField(default=False)
    posted_by = models.ForeignKey(company_profile, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Job_Post"


class Job_Skill(models.Model):
    job = models.ForeignKey(Job_Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=15)


class Document(models.Model):
    file = models.FileField(upload_to='photos/%Y/%m/%d', validators=[validate_file_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Resume(models.Model):
    applicantID = models.ForeignKey(Applicant, on_delete=models.CASCADE, unique=True)  # Foreign key from Applicant table
    resume_summary = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
# a = Resume(applicantID=request.user,resume_summary=request.POST['summary'])
# a.save()
# resumed_id = a


class Resume_Skills(models.Model):
    resumeID = models.ForeignKey(Resume, on_delete=models.CASCADE)  # Foreign key from Applicant table
    skill_names = models.CharField(max_length=255, blank=True)
# for i in request.POST.get_lines('resume'):
#     Resume_Skills(skill_names=i, resumeID=resumed_id)


class Resume_Education(models.Model):
    resumeID = models.ForeignKey(Resume, on_delete=models.CASCADE)  # Foreign key from Applicant table
    name = models.CharField(max_length=255, blank=True)
    institute_name = models.CharField(max_length=255, blank=True)
    start = models.CharField(max_length=255, blank=True)
    end = models.CharField(max_length=255, blank=True)


class Resume_Experience(models.Model):
    resumeID = models.ForeignKey(Resume, on_delete=models.CASCADE)  # Foreign key from Applicant table
    title = models.CharField(max_length=255, blank=True)
    start = models.CharField(max_length=255, blank=True)
    end = models.CharField(max_length=255, blank=True)


class Resume_Activities(models.Model):
    resumeID = models.ForeignKey(Resume, on_delete=models.CASCADE)  # Foreign key from Applicant table
    title = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)


class AppliedJobs(models.Model):

    class ApplicationStatus(models.TextChoices):
        PENDING = 'PD', _('Pending')
        ACCEPTED = 'AC', _('Accepted')
        REJECT = 'RJ', _('Rejected')

    status = models.CharField(
        max_length=2,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.PENDING,
    )
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    job = models.ForeignKey(Job_Post, on_delete=models.CASCADE)
    resume = models.ForeignKey(Document, on_delete=models.CASCADE)
