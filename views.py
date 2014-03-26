from flask import Blueprint, render_template, request, redirect, url_for
from models import Post,User, Comment, db
from wtforms import form, fields, validators
from flask.views import MethodView
from flask.ext import login,admin
from wtforms.fields import TextAreaField,TextField
from flask.ext.admin.contrib.mongoengine import ModelView
from flask.ext.mongoengine.wtf import model_form

POST_PER_PAGE = 1

posts = Blueprint('posts', __name__, template_folder='templates')


class ListView(MethodView):
	
    def get(self):
	page = int(request.args.get('page', 1))
	posts = Post.objects.paginate(page = page, per_page = POST_PER_PAGE)
	return render_template('posts/list.html', posts = posts, endpoint = request.endpoint, view_args = request.view_args)

   

class DetailView(MethodView):

    form = model_form(Comment, exclude=['created_at'])


    def get_context(self, slug):
        post = Post.objects.get_or_404(slug=slug)
	form = self.form(request.form)

        context = {
            "post": post,
	    "form": form
        }
        return context

    def get(self, slug):
        post = Post.objects.get_or_404(slug=slug)
        return render_template('posts/detail.html', post=post)

    def post(self,slug):
 	context = self.get_context(slug)
	form = context.get('form')
	
	comment = Comment()
        form.populate_obj(comment)
	post = context.get('post')
	post.comments.append(comment)
	post.save()
	
        return redirect(url_for('posts.detail', slug=slug))


class PostView(ModelView):
    create_template = 'edit.html'
    edit_template = 'edit.html'


    

# Register the urls
posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/archives/<slug>/', view_func=DetailView.as_view('detail'))


