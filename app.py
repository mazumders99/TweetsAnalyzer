
from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

from matplotlib.style import use
from platformdirs import user_state_dir
from forms import UserForm, TwitterSearchForm, LoginForm, MootsForm, AddFavorite
import twitter_bot_python as bot
import twitter_bot_test as bot2
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zfldepccsydywe:199084877f6571c67b03c4b5ba0aa0fd6dc3a4db7e46bc54645bdcc01d9657ad@ec2-52-22-136-117.compute-1.amazonaws.com:5432/db00s6gbl9viqd'
app.config['SECRET_KEY'] = "e07e5ecdb25b94b71947500f166ce38e"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class TwitterUsers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    submitter_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    moots = db.relationship('TwitterUsers', backref='submitter')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return '<Name %r>' % self.name


@app.route('/analyse_tweets', methods=['GET', 'POST'])
def analyse_tweets():
    not_well_classified = False
    form = TwitterSearchForm()
    if form.validate_on_submit():
        username = form.username.data
        number_of_tweets = form.number_of_tweets.data
        # x_coord, y_coord = bot.plot_graph(username, number_of_tweets)
        # x_coord, y_coord, tweets_dict = bot2.plot_graph(
        #     username, number_of_tweets)

        try:
            x_coord, y_coord, tweets_dict = bot2.tweets_analysis(
                username, number_of_tweets)
            data = {}
            for i in range(7):
                data[x_coord[i]] = y_coord[i]

            if y_coord[1] < 5:
                not_well_classified = True
            # return render_template('charts.html', data=data)
            # imgpath = bot2.get_profile_info(username)
            user_info_dict = bot2.get_profile_info(username)
            return render_template('result.html', username=username, x_coord=x_coord, y_coord=y_coord, data=data, tweets_dict=tweets_dict,
                                   number_of_tweets=number_of_tweets, not_well_classified=not_well_classified, img_path=user_info_dict['profile_img_url'])
        except:
            flash(
                "Couldn't get data for the username you entered <html>&#128557;</html>  Are you sure the account exists and is public?")
            return render_template('analyse_tweets.html', form=form)
    return render_template('analyse_tweets.html', form=form)

# Fav users start


@app.route('/analyse_tweets_for/<string:username>', methods=['GET', 'POST'])
def analyse_tweets_for(username):
    not_well_classified = False
    form = TwitterSearchForm()

    try:
        x_coord, y_coord, tweets_dict = bot2.tweets_analysis(
            username, 200)
        data = {}
        for i in range(7):
            data[x_coord[i]] = y_coord[i]
        # return render_template('charts.html', data=data)

        if y_coord[1] < 5:
            not_well_classified = True
        print(not_well_classified)
        user_info_dict = bot2.get_profile_info(username)
        return render_template('result.html', username=username, x_coord=x_coord, y_coord=y_coord, data=data, tweets_dict=tweets_dict,
                               number_of_tweets=200, not_well_classified=not_well_classified, img_path=user_info_dict['profile_img_url'])
    except:
        flash(
            "Couldn't get data for the username you entered <html>&#128557;</html>  Maybe this account isn't public anymore!")
        return render_template('analyse_tweets.html', form=form)
    return render_template('analyse_tweets.html', form=form)


# Fav users end

@app.route('/charts', methods=['GET', 'POST'])
def display_charts():

    data = {}
    x_coord, y_coord = bot.plot_graph('fabrizioromano', 200)
    # for i in range(6):
    #     data[topic_names[i]] = topic_mentions[i]
    for i in range(7):
        data[x_coord[i]] = y_coord[i]

    # data = {'topic': 'mentions', 'ronaldo': 32, 'messi': 25,
    #         'cristiano': 21, 'league': 9, 'madrid': 6, 'united': 5}

    return render_template('charts.html', data=data)
    # return render_template('charts.html', arr=arr)


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def index():
    form = UserForm()

    # return render_template('test.html', form=form, website_users=website_users)

    #

    # website_users = Users.query.order_by(Users.date_added)
    return render_template('test.html', form=form)
    # return render_template('index.html', anime_list=anime_list, form=form, website_users=website_users)
    #


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(name=form.username.data).first()
        if user is None:
            hashed_pw = generate_password_hash(
                form.password_hash.data, "sha256")
            user = Users(name=form.username.data,
                         email=form.email_id.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()

        form.username.data = ''
        form.email_id.data = ''
        form.password_hash.data = ''
        form.password_hash2.data = ''
        flash("User added successfully!")

    website_users = Users.query.order_by(Users.date_added)
    return render_template('register.html', form=form, website_users=website_users)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(name=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password_hash.data):
                login_user(user)
                flash('Login Successful!')
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong password :( Try again!!')
        else:
            flash("User doesn't exist!! (yet, but you can change that! ;))")
    website_users = Users.query.order_by(Users.date_added)
    return render_template('login.html', form=form, website_users=website_users)


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Logged out! You can no longer see your dashboard T__T")
    return redirect(url_for('login'))


@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

# Search user start


@app.route("/search_user", methods=['GET', 'POST'])
def search_user():
    form = MootsForm()
    moot_name = None
    user_info_dict = None

    if form.validate_on_submit():

        user_info_dict = bot2.get_profile_info(form.username.data)
        if user_info_dict is not None:
            moot_name = user_info_dict['screen_name']

        else:
            flash("That username either doesn't exist on Twitter, or has been removed!")

    # if form2.validate_on_submit():
    #     existing_moot = TwitterUsers.query.filter_by(
    #         user_name=form.username.data, submitter_id=current_user.id).first()
    #     if existing_moot is None:
    #         return redirect(url_for('add_user_as_favorite', username=user_info_dict['screen_name']))

    moots = TwitterUsers.query.order_by(TwitterUsers.date_added)
    return render_template('search_user.html', moots=moots, form=form, user_info_dict=user_info_dict, username=form.username.data)


@app.route("/search_for/<username>", methods=['GET', 'POST'])
@login_required
def search_for(username):
    form = MootsForm()
    # user_info_dict = None

    user_info_dict = bot2.get_profile_info(username)

    if user_info_dict is not None:
        moot_name = user_info_dict['screen_name']
    else:
        flash("That username either doesn't exist on Twitter, or has been removed!")

    moots = TwitterUsers.query.order_by(TwitterUsers.date_added)
    return render_template('search_user.html', moots=moots, form=form, user_info_dict=user_info_dict, username=None)


# Search user end


@app.route('/add_favorite/<username>', methods=['GET', 'POST'])
@login_required
def add_user_as_favorite(username):
    form = AddFavorite()
    submitter = current_user.id

    existing_moot = TwitterUsers.query.filter_by(
        user_name=username, submitter_id=current_user.id).first()
    if existing_moot is None:
        twitter_user = TwitterUsers(
            user_name=username, submitter_id=submitter)
        db.session.add(twitter_user)
        db.session.commit()
        flash("Added as favorite!")
    else:
        flash("User already exists as a favorite!")
    moots = TwitterUsers.query.order_by(TwitterUsers.date_added)
    return render_template('favorites.html', username=username, moots=moots)


@app.route('/remove_from_favorites/<username>', methods=['GET', 'POST'])
@login_required
def remove_user_from_favorites(username):
    # return render_template('tandc.html')
    user_to_remove = TwitterUsers.query.filter_by(
        user_name=username, submitter_id=current_user.id).first()
    db.session.delete(user_to_remove)
    db.session.commit()
    flash("User removed from favorites!")
    moots = TwitterUsers.query.order_by(TwitterUsers.date_added)
    return render_template('favorites.html', username=username, moots=moots)
    # return render_template('tandc.html')


@app.route('/favorites', methods=['GET', 'POST'])
@login_required
def favorites():
    moots = TwitterUsers.query.order_by(TwitterUsers.date_added)
    return render_template('favorites.html', moots=moots)


@app.route('/view_user/<username>',  methods=['GET', 'POST'])
@login_required
def view_user(username):
    user_info_dict = bot2.get_profile_info(username)

    if user_info_dict is None:
        flash("That username either doesn't exist on Twitter, or has been removed!")

    moots = TwitterUsers.query.order_by(TwitterUsers.date_added)
    return render_template("viewuser.html", moots=moots, user_info_dict=user_info_dict)


@app.route('/resources')
def resources():
    return render_template('resources.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/termsandconditions')
def termsandconditions():
    return render_template('tandc.html')


@app.route('/privacypolicy')
def privacypolicy():
    return render_template('privacypolicy.html')


@app.route('/coming-soon')
def coming_soon():
    return render_template('comingsoon.html')


@app.route('/test2')
def test2():
    return render_template('test2.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
