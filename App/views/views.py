from flask import Blueprint, render_template, request
from ..models.models import *

blog = Blueprint('user', __name__)


# blog home page
@blog.route('/')
@blog.route('/index')
def blog_index():
    categorys = CategoryModel.query.all()
    return render_template('home/index.html', categorys=categorys)
