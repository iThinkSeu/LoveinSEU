__author__ = 'liewli'

from flask import Blueprint, render_template, abort
from jinja2 import  TemplateNotFound

Share = Blueprint('post_share', __name__, template_folder="templates", static_folder="static", url_prefix="/post_share")

@Share.route('/<postid>', methods=['POST'])
def show(postid):
    try:
        return render_template('post.html')
    except TemplateNotFound:
        abort(404)