from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from modules.posts.forms import PostForm
from modules.models import Post
from modules import db


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
@main.route('/home')
def home():
    form = PostForm()
    if(form.validate_on_submit()):
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template('home.html', posts=posts, title="Home", form=form)


@main.route('/about')
def about():
    return render_template('about.html', title="About")

