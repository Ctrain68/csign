from flask import render_template, request, Blueprint, flash, redirect, url_for, abort
from src.models import SignIn, User
from src import db
from src.users.forms import SignInForm

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home", methods=['GET','POST'])
def home():
    return render_template('home.html')


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/signin/<string:business_name>", methods=['GET', 'POST'])
def sign_in(business_name):
    form = SignInForm()
    try:
        business = User.query.filter_by(business_url=business_name).first()
        if form.validate_on_submit():
            signIn = SignIn(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                phone=form.phone_number.data,
                symptoms=form.symptoms.data,
                signup=form.sign_up.data,
                user_id=business
            )
            db.session.add(signIn)
            db.session.commit()
            flash('You have been signed in!', 'success')
            # redirect to menu
            if business.menu_url:
                return redirect(business.menu_url)
            return render_template('signin.html', logo=logo, business_name=b_name, form=form)
        elif request.method == 'GET':
            logo = url_for('static', filename='profile_pics/' + business.logo)
            b_name = business.business_name
            return render_template('signin.html', logo=logo, business_name=b_name, form=form)

    except:
        return render_template('errors/404.html'), 404
    logo = url_for('static', filename='profile_pics/' + business.logo)
    b_name = business.business_name
    return render_template('signin.html', logo=logo, business_name=b_name, form=form)
