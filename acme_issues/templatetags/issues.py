from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from acme_issues.models import IssueCategory

register = template.Library()

@register.filter(needs_autoescape=True)
def render_question_tree(question, autoescape=True):
	e = conditional_escape if autoescape else lambda x: x
	return mark_safe(recurse_tree(question, e))

def recurse_tree(question, escape):
	if question is None:
		return render_input()
	
	if type(question) == IssueCategory:
		return render_category(question, escape)

	markup = """
<div data-id="{id}" class="qb_question">
		<button class="btn btn-danger btn-xs remove_question"><span class="glyphicon glyphicon-remove"></span></button>
		<span class="qb_question_title">{question}</span>
		<ul>
			<li class="yes">{yes}</li>
			<li class="no">{no}</li>
		</ul>
</div>
"""
	yes = recurse_tree(question.get_yes(), escape)
	no = recurse_tree(question.get_no(), escape)

	return markup.format(id=question.id, question=question.question, yes=yes, no=no)

def render_category(category, escape):
	t = """<div><button class="btn btn-danger btn-xs remove_category"><span class="glyphicon glyphicon-remove"></span></button> <span class="qb_category">{name}</span></div>"""
	return t.format(name=escape(category.name), id=escape(category.id))

def render_input():
	return """<div class="input-group" style="width:300px">
	<input type="text" class="form-control new_text" placeholder="Add question or category...">
	<span class="input-group-btn">
		<button class="btn btn-primary save_button" type="button"><span class="glyphicon glyphicon-plus"></span></button>
	</span>
</div>"""