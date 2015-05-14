from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotAllowed
from django.template import RequestContext, loader
from models import *
import json

##### General
def render_template(request, template, context):
    template = loader.get_template(template)
    context = RequestContext(request, context)
    return template.render(context)

# Create your views here.
def show_question(request, source):
	s = IssueSource.objects.get(name__iexact=source)
	questions = CategoryQuestion.objects.all()
	roots = []
	for q in questions:
		if q.is_root():
			roots.append(q)
	return HttpResponse(render_template(request, "issues/questions.html", {"source":s, "root_questions":roots}))

from templatetags.issues import render_question_tree

def create_question(request):
	if request.method == "POST":
		data = request.body
		parsed = json.loads(data)
		if "text" not in parsed:
			return HttpResponseBadRequest(json.dumps({"reason":"No text provided for question"}))
		text = parsed["text"]
		q = CategoryQuestion(question=text)
		q.save()
		
		response = {
			"id": q.id,
			"question": q.question,
			"html": render_question_tree(q)
		}

		if "parent" in parsed:
			p = CategoryQuestion.objects.get(parsed["parent"])
			if parsed["yes"]:
				p.set_yes(q)
			else:
				p.set_no(q)
			response["parent"] = p.id
			response["yes"] = parsed["yes"]

		return HttpResponse(json.dumps(response))
	else:
		return HttpResponseNotAllowed(["POST"])