from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(needs_autoescape=True)
def render_question_tree(question, autoescape=True):
	e = conditional_escape if autoescape else lambda x: x
	return mark_safe(recurse_tree(question, e))

def recurse_tree(question, escape):
	if question is None:
		return ""
	markup = """
<ul data-id="{id}" class="qb_question">
	<li>
		<span class="qb_question_title">{question}</span>
		<ul>
			<li class="yes">{yes}</li>
			<li class="no">{no}</li>
		</ul>
	</li>
</ul>
"""
	if question.yes is not None and question.yes_type == "category":
		yes = """<span class="qb_category" data-id="{id}">{name}</span>"""
		y = question.get_yes()
		yes = yes.format(name=escape(y.name), id=escape(y.id))
	else:
		yes = recurse_tree(question.yes, escape)

	if question.no is not None and question.no_type == "category":
		no = """<span class="qb_category" data-id="{id}">{name}</span>"""
		n = question.get_no()
		no = no.format(name=escape(n.name), id=escape(n.id))
	else:
		no = recurse_tree(question.no, escape)

	return markup.format(id=question.id, question=question.question, yes=yes, no=no)