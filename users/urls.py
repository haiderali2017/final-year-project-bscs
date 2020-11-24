from django.urls import path, include
from .views import *
app_name = "users"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="index_job_posting"),
    path('users/', include('django.contrib.auth.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('company_dashboard', login_required(CompanyDashboard.as_view()), name='company_dashboard'),

    path('total_jobs_posted', login_required(total_jobs_posted.as_view()), name='total_jobs_posted'),

    path('Edit_Company_Profile', login_required(CompanyProfileView.as_view()), name='Edit_Company_Profile'),
    path('post_a_job', login_required(JobPostView.as_view()), name='post_a_job'),
    path('List_all_jobs', login_required(JobListCompanyView.as_view()), name='List_all_jobs'),
    path('application/<int:id>/<str:status>',login_required(ApplicationStatusChange.as_view()), name='set_application_status'),
    path('view_latest_jobs',login_required(LatestJobsView.as_view()), name='view_latest_jobs'),

    path('LatestJobsupdatedView', login_required(LatestJobsupdatedView.as_view()), name='LatestJobsupdatedView'),
    path('single_company_jobs/<int:id>', login_required(single_company_jobsView.as_view()), name='single_company_jobs'),
    path('list_all_job_userEnd', login_required(JobListUserView.as_view()), name='view_all_jobs'),
    path('user_single_job_detail/<int:id>', login_required(JobDetailUserView.as_view()), name='user_single_job_detail'),
    path('edit_a_job/<int:id>', login_required(JobEditView.as_view()), name='edit_a_job'),
    path('delete/<int:pk>',JobDeleteView, name='delete_a_job'),
    # path('delete/<int:pk>', login_required(JobDeleteView.as_view()), name='delete_a_job'),
    path('blank', login_required(UserResumeView.as_view()), name="blank"),
    path('company_registration_form', (CompanyRegisterView.as_view()), name="company_registration_form"),
    path('login_form', LoginView.as_view(), name="login_form"),
    # job_posting URLS
    path('dashboard_job_posting', login_required(DashBoardUserView.as_view()), name='dashboard_job_posting'),
    path('applied_jobs', login_required(AppliedJobsView.as_view()), name='applied_jobs'),
    path('delete_education/<int:id>', ResumeEducationDelete, name='delete_education'),
    path('delete_experience/<int:id>', ResumeExperienceDelete, name='delete_experience'),
    path('all_applications', login_required(all_applicationsView.as_view()), name='all_applications'),
    path('shortlisted', login_required(shortlistedView.as_view()), name='shortlisted'),
    path('rejected_application', login_required(rejected_applicationView.as_view()), name='rejected_application'),
    path('profile/<int:id>', login_required(ProfileUserView.as_view()), name='profile'),
    path('cv_builder_tool_job_posting', login_required(ResumeBuilderView.as_view()), name='cv_builder_tool_job_posting'),
    path('about_us_job_posting', AboutUSJobView.as_view(), name='about_us_job_posting'),
    path('contact_job_posting', ContactJobView.as_view(), name='contact_job_posting'),
    # File upload urls
    path('file', model_form_upload, name='file_upload'),





    # path('cv_design_job_posting', cv_design_job_posting, name='cv_design_job_posting'),
    # path('register_job_posting', register_job_posting, name='register_job_posting'),
    # path('dashboard', TemplateView.as_view(template_name='Dashboard.html'), name='dashboard'),
    # path('cv_design', cv_design, name="cv_design"),




    # path('model_form_upload', model_form_upload, name='model_form_upload'),
    # path('basic-upload', BasicUploadView.as_view(), name='basic_upload'),
    # path('progress-bar-upload', ProgressBarUploadView.as_view(), name='progress_bar_upload'),
    # path('drag-and-drop-upload', DragAndDropUploadView.as_view(), name='drag_and_drop_upload'),
]

# urlpatterns = [

# Job_posting URLS
# path('users/', include('users.urls')),
# path('admin/', admin.site.urls),
# path('register_page', register_page, name='register_page'),
# # path('job_listings', job_listings, name='job_listings'),
# # path('edit/<int:id>', edit),
# # path('edit', edit, name='edit'),
# path('users/', include('users.urls')),

# ]