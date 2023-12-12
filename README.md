# email_automation
This project is related to scheduling emails for each subscribers and to make it periodic for a given frequency as well as given periodic gap.
# Table of Contents
+ [About](#description)
  + [Subscriber](#subscriber)
  + [Email](#email)
  + [Email History](#Email_History)
  + [API](#api)
+ [Technologies Used](#built_with)
+ [Getting Started](#getting_started)
  + [Installation](#installation)
  + [Run](#run)


## About <a name="description"></a>

>> ### Subscriber<a name="subscriber"></a>
+ Displayed a list of subscriber with basic information (name, email) in a table format. 
+ Provided a form for users to add new subscriber (on top right). Fields include name, email.
+ Implemented a update button to allow users to edit subscriber details and save the changes.

>> ### Email <a name="email"></a>
+ To schedule email for individual,implemented a form with field of subject,message,scheduling time,periodicity gap and frequency.

+ For each user multiple email can be scheduled by clicking 'Create New' button which is inside scheduleemail(from Home page).
+ These scheduled emails's field  like email content, scheduling time,periodicity and frequency can be change using 'Change' button.
+ All scheduled emails can be view and delete using View, Delete button respectively.
+ First navigate inside ChangeSchedule(from Home page) to perform above activity.

>>### Email History <a name="Email_History"></a>
+ A history of sent email with field of timestamp,sender,recipient,subject, and body text has been generated for each user individually in descending order of time.

+ For upcoming scheduled email a record is also generated which can be view using scheduled emails button at Home Page

>>### API <a name="api"></a>
+ An API of subscriber with information of name and Emails are created that can be accessed from 'Subscriber API' button at top of Home Page
+ An another nested api of scheduled email is created with information of subscriber(to whom it has sent) and emails content.
+ A another nested api of sent email( past)for history is created with information of subscriber(to whom it has sent) and emails content.
  
## Technologies Used <a name="built_with"></a>
Website:
+ HTML
+ CSS 
+ JS
+ Django
+ Python
+ SQLITE

## Getting Started <a name="getting_started"></a>
### Installation <a name="installation"></a>
The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/sumit5529/email_automate.git
$ cd per_email
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ pip install virtualenv
$virtualenv env
$ env/scripts/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements
```

one thing more,you have to changes in database in setting file 
update the id and password of DB according you.


### Run <a name="run"></a>
Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd per_email
(env)$ python manage.py runserver

```
Run in another two different terminal one for scheduling and second for worker
```sh
(env) celery -A per_email beat -l info    
(env)$ celery -A per_email.celery worker --pool=solo -l info 
```
And navigate to `http://127.0.0.1:8000`.

Now schedule the Email.