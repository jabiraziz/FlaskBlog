# FlaskBlog
This Fully authenticated blog web-application is created using Flask and boostrap.
Flask is a micro-web app framework based upon Python while boostrap is just a free CSS library
that helps you make your website look cool and attactive.

To access the main or home page you need to register yourself first, login and then go to home page.
From home page user can create a new post or update the existing post.

Also if user has forgotten his/her password then all he/she needs to do is to click on forgot password,
and from there a new token will be generated which will give the user control to create a new password.

with that being said let's have a look at code , i have created mainly three python files: models.py, form.py and init.py.
models.py file contain all the database tables that we need, in this scenrio User and Post are 2 two tables that we have
created .These tables will help us to store differen records, for instance what is the post? who is the
author of the post ? what was the time when a post was posted? etc...
Moreover, i have used  SQLAlchemy(it is basicall ORM) database which makes it very easy for python developer
to work with the tables and relationships(Database).

forms.py contain all the form of our application. RegistrationForm, LoginForm and AccountUpdateForm form are actually 
coded in this files.
wtfroms and wtforms.validator module makes it easy and comfortable to work the forms in flask.

init.py file is used to intialize our web app using app = Flask(__name__) statement,
                                  our databse using app - SQLalchemy(db) statement.
                                  
also there is one more important file names run.py which helps to run our flask.
and make sure that the debug mode is off in production.
use below statement to make it turn off:
if __name__ == "__main__":
    app.run(debug=False)
    
Also i have made certain restrictions i.e Every User must have a different email address, User needs to be register 
before Posting or accessing the actual ap, User cannot update someone else's Post and more ...
