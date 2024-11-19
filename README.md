# Interview Managament Tool

### Objective:

 A tool to save and plan interview related information ideal for a organisation
 that wants to host such a system under its it own hood.

### Packages used:

- Backend: Django 4.x
- Frontend: Bootstrap 3.7

### Running the project
- With either django command on shell:

  `python manage.py runserver`
- With docker
  - Build image:
    `docker compose build`
  - Run container:
    `docker compose up -d`


### Interview Management System:

  - Schedule Interview for a Candidate. **[Completed]**
  - Add Rounds to a Interview and assign to an interviewer. Leave additional instructions if required **[Completed]**
  - Rounds can have optional assisting interviewers too. **[Completed]**
  - See complete history of a Candidate (All interviews, rounds with results). **[Completed]**
  - See complete history of a Interviewer (All rounds with rating link). **[Completed]**
  - Add Ratings based on Aspects for each Round. **[Completed]**
  - Rating Sheet shows comments and points received along with a a graph showing comparison
    between expected points and actual points. **[Completed]**
  - Global Search in NavBar that can search for Candidates, Vendors, Users, and Positions. **[Completed]**
  - Downloadable reports in Excel form. **[Completed]**
  - Statistics **[Completed]**
  - Calender: Month wise showing dates with links for all interviews that day. **[Completed]**
  - Bulk Create Candidates - This feature can be used during Interview Drives where we need to create lots of candidates for a common positions and they have the same sequence of rounds . **[Completed]**
  - Upload resume through Candidate details page, after you have created a candidate. If a resume (any document is present), the same can be viewed through Candi details page.**[Completed]**
  
  ### Possible Ideas:
  - Browser Notifications when a round is scheduled in someone's name.
  - Share Button beside Rating sheet . We can launch a modal with multi-selectable users , then send mail with attachment.
  - Auto send Rating Sheet to a selected Users (e.g may be HR).
  - If a Interview is being created for user, check if previous interview for candidate was closed. 
  - Auto send interview reminder email.

  # Next release plan:
  - APIs (ViewSets and serializers)
  - unittests
  - coverage
  - celery setup
  - memcache settings
  - optimize queries
