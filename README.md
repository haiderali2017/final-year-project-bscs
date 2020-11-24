# Intelligent Candidate Shortlister (Final Year Project)
# Installation instructions
    1. Install Python from https://www.python.org/downloads/
    2. Install PyCharm from https://www.jetbrains.com/pycharm/
    3. Open PyCharm.
    4. Click File on top left and then click Open.
    5. In source_code folder, open faseehFYP-master folder.
    6. Click Terminal in bottom left panel.
    7. Type new_env\Scripts\activate
    8. Type python manage.py runserver
    9. Click http://127.0.0.1:8000/

# User manual
    1. Signing up as Company
        a. After running the project in browser, click Login button on top right.
        b. Click Sign Up link straight against New Company.
        c. Enter Sign Up credentials. Make sure password has 
            ▪ Minimum 8 letters
            ▪ One special character 
            ▪ One capital case letter

    2. Post jobs through Company Dashboard
        a. Click Manage Jobs on left navigation bar.
        b. Click Post a Job.
        c. Fill up Job details. 
        d. Log out.

    3. Signing up as Admin
        a. Go to URL field of browser and type http://127.0.0.1:8000/admin 
        b. Enter admin as Username and 123 as Password.

    4. Approving Jobs through Admin Dashboard
        a. Click the link Job_posts under Users section.
        b. Click the checkbox of newly added job(s). Newly added jobs are marked red under Status column.
        c. Click the dropdown and select Mark selected Jobs as published.
        d. Click Log out on top right.

    5. Signing up as User
        a. Click Sign Up link straight against New Candidate.
        b. Enter Sign Up credentials. Make sure password has 
            ▪ Minimum 8 letters
            ▪ One special character 
            ▪ One capital case letter

    6. Building CV
        a. Click Manage CV on left navigation bar.
        b. Click CV Builder Tool.
        c. Fill up the details and click Save. Due to smaller dataset, make sure the following 2 things must match with the job details which the company added. Otherwise, the jobs will not be displayed on User Dashboard.
            ▪ Location text field
            ▪ Skills

    7. Applying for jobs
        a. Click Jobs on left navigation bar.
        b. Click Latest Jobs.
        c. There are two ways to apply for jobs. 
            ▪ Location – Select dropdown and choose the city. Next, click submit.
            ▪ Company – Click on Search Jobs by Company. Click on one of the companies.
        d. Click on one of the jobs.
        e. Click Apply.
        f. Upload a CV in PDF or Doc extension.

    8. Looking for Applied Jobs
        a. Click Jobs on left navigation bar.
        b. Click My Applied Jobs.
        c. This page will show jobs after Acceptance or Rejection from company’s end.
        d. Log out.

    9. Parsing and Ranking CVs through Company Dashboard
        a. Enter login details of registered companies.
        b. Click Manage Jobs on left navigation bar.
        c. Click List all Jobs.
        d. Click Applications button at the end of a single job.
        e. Click Parsed Data. It will show all the extracted information out of a resume.
        f. If extracted information matches with job details, click Accept otherwise Reject.

# Research Material 
    1. Satyaki Sanyal, Souvik Hazra, Soumyashree Adhikary, Neelanjan Ghosh, “Resume Parser with Natural Language Processing”
    2. Sayed Zainul Abideen Mohd Sadiq, Juneja Afzal Ayub, Gunduka Rakesh Narsayya, Momin Adnan Ayyas, Prof. Khan Tabrez Mohd. Tahir, “Intelligent Hiring with Resume Parser and Ranking using Natural Language Processing and Machine Learning”
    3. https://medium.com/@divalicious.priya/information-extraction-from-cv-acec216c3f48
    4. https://www.nltk.org/book/ch07.html
