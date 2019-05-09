from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from flaskblog import bcrypt, db
from flaskblog.models import Post, User
from flaskblog.users.forms import LoginForm, RequestResetForm, ResetPasswordForm, SignupForm, UpdateAccountInformationForm
from flaskblog.users.utils import save_avatar, send_reset_email

users = Blueprint('users', __name__)

@users.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! Now you can login!', 'success')
        return redirect(url_for('users.login'))
    return render_template('signup.html', title='Signup New Pythonista', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        flash('Access denied!', 'danger')
    return render_template('login.html', title='Login Pythonista', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountInformationForm()
    if form.validate_on_submit():
        if form.avatar.data:
            avatar_picture = save_avatar(form.avatar.data)
            current_user.avatar = avatar_picture

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Information was Updated', 'info')
        return redirect(url_for('users.account'))
    
    form.username.data = current_user.username
    form.email.data = current_user.email
    avatar_src = url_for('static', filename='images/account/' + current_user.avatar)
    return render_template('account.html', title='Account', avatar_src=avatar_src, form=form)

@users.route('/author/<string:username>')
def author_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query\
        .filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('author-posts.html', posts=posts, user=user, title=f'All posts of {user.username}')

@users.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Confirmation link has been sent on your email!', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset-request.html', form=form, title='Request Reset Password')

@users.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    user = User.verify_reset_token(token)

    if user is None:
        flash('This is invalid or expired token!', 'warning')
        return redirect(url_for('users.reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! Now you can login!', 'success')
        return redirect(url_for('users.login'))
    
    return render_template('reset-password.html', form=form, title='Enter new password for your account')
