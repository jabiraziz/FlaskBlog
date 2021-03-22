import os
import secrets
# PIL or pillow will help us to work with picture (resize,rotate etc)
from PIL import Image
# url_for will found the exact location for us
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             PostForm, RequestResetForm, ResetPasswordForm)
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route('/')
@app.route("/home")
def home():
    # grab the page that we want,default page is 1, page number must be integer
    page = request.args.get('page', 1, type=int)
    """Pagination helps us to divide posts into different or multiple pages
    (Post.date_posted.desc()) this query will help us to bring the latest post
    to the top."""
    # This query will grab all the post related data from database and will display it on home.
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # create instance of RegistrationForm()
    form = RegistrationForm()
    if form.validate_on_submit():
        """Hashing the password will help us not to access the
        exact password that user entered, instead show us the
        hashed vesion of the password (hashed Hexa -decimal value)."""
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # check if the email is matching with the email which is already in database
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # login_user is a function , it also takes remember option too
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    # logout_out is the function
    logout_user()
    return redirect(url_for('home'))


# the argument is the actual picture form data
# this function will save the user uploaded picture to our file system
def save_picture(form_picture):
    """ random_hex will randomize the name of the file or uploaded file and that's because
    we may have multiple picture with same name and they might collide. """
    random_hex = secrets.token_hex(8)
    """Os module here will help us to save that picture will the uploaded extension.
    it either be jpg or png. os.path.splitext() this statement will help us with that.
    this function return two values.....1)filename without extension and 2) extension itself
    form_picture passed as a parameter is gonna be the data from the field that the user submit."""
    _, f_ext = os.path.splitext(form_picture.filename)
    # combine the random hex with the file extension
    picture_fn = random_hex + f_ext
    # create the full path that where the file will be saved or stored
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    """we will resize the uploaded picture 'cause high pexels picture
    may slow down our website"""
    output_size = (128, 128)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    # Now save the actual picture.
    i.save(picture_path)

    return picture_fn


# @login_required means that the user must be logged in to access has account
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # check if there is any profile picture.
        if form.picture.data:
            # set the profile picture.
            # save picture() is the function
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        # As the data is entered into form So that's why its form.username.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        # Populate the fields with the current_user data
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # grab the data(title,content and author) from the new post form
        # this will add the actual post related data into database.
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


# this will take us to a specific post
@app.route("/post/<int:post_id>")
def post(post_id):
    # query all the posts, if the post is found Good if not show no found url page
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # to make sure that only the authorize user can update the post
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        # Update the post
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        # Populate form with the existance data.
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """if the one who is deleting post is not the current user the
    display the abort error.
    HTTP 403 means that the access to the requested resource or page is forbidden """
    # run the query ,
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


# show posts of the specific user
@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    # get the user
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


def send_reset_email(user):
    # get the token from the user model
    token = user.get_reset_token()
    """Message class helps to create an email.
    first is subject line,
    2nd in sender use such email that is not related to anyone. otherwise it may cause spam."""
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


"""in the below route user will enter their email address in order
to reset their password"""


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # make sure that the user is logged out before resetting their password
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


"""in the below route user will actually reset their password
with the token"""


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # Verify the token (we have user here already)
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    # Now the user is valid then show him the form
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # now hash the new password also
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
