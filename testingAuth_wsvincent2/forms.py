from django.contrib.auth.forms import UserCreationForm
from users .models import Job_Post

class Job_PostCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Job_Post
        fields = ('Job_title','job_designation','Job_Description','qualification_required',
                  'positions', 'experience_required','Contact_Number', 'Country', 'Region',
                  'gender_preference', 'job_nature','City')