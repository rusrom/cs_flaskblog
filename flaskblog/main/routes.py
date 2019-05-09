from flask import render_template, request, Blueprint
from flaskblog.models import Post


main = Blueprint('main', __name__)

@main.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    # posts = Post.query.paginate(page=page, per_page=2)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # posts = Post.query.all()
    return render_template('home.html', posts=posts, title='rusrom\'s main')

@main.route('/about')
def about():
    return render_template('about.html', title='About rusrom')