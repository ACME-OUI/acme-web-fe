from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotAllowed
from django.template import RequestContext, loader
from models import *
import json

# Decorator that passes parsed HTTP body as a kwarg (json_data=) if it's present
def expects_json(f):
	def wrapper(request, *args, **kwargs):
		if request.META.get("CONTENT_TYPE", None) == "application/json":
			data = request.body
			data = json.loads(data)
			kwargs["json_data"] = data
		return f(request, *args, **kwargs)
	return wrapper


##### General
def render_template(request, template, context):
    template = loader.get_template(template)
    context = RequestContext(request, context)
    return template.render(context)

def make_issue(request):
	questions = CategoryQuestion.objects.all()
	roots = [q for q in questions if q.is_root()]
	return HttpResponse(render_template(request, "issues/issue.html", {"root_questions":roots}))

def get_next(request, id):
	try:
		q = CategoryQuestion.objects.get(id=id)
		data = request.GET

		if "yes" not in data:
			print "defaulting to true"
			yes = True
		else:
			yes = data["yes"] == "true"

		if yes:
			q = q.get_yes()
		else:
			q = q.get_no()
		
		data = {"id": q.id}
		
		if type(q) == CategoryQuestion:
			data["question"] = q.question
		else:
			data["category"] = q.name

		return HttpResponse(json.dumps(data))

	except CategoryQuestion.DoesNotExist:
		return HttpResponseBadRequest(json.dumps({"reason":"Question %d does not exist" % id}))
	except AttributeError:
		return HttpResponseBadRequest(json.dumps({"reason":"Question %d has no %s value" % (int(id), "yes" if request.GET["yes"] else "no")}))

# Create your views here.
def show_question(request, source):
	s = IssueSource.objects.get(name__iexact=source)
	# Root question of every group of categories has no "no" value.
	questions = CategoryQuestion.objects.filter(no=None)
	questions = CategoryQuestion.objects.all()
	roots = [q for q in questions if q.is_root()]
	return HttpResponse(render_template(request, "issues/questions.html", {"source":s, "root_questions":roots}))

from templatetags.issues import render_question_tree
def edit_question(request, id):
	if request.method != "POST":
		return HttpResponseNotAllowed(["POST"])
	try:
		q = CategoryQuestion.objects.get(id=id)

		data = json.loads(request.body)
		
		if data["name"] is None:
			c = None
		else:
			c = IssueCategory.objects.get(name=data["name"], source__name=data["source"])

		if data["yes"]:
			q.set_yes(c)
		else:
			q.set_no(c)
		q.save()

		return HttpResponse(json.dumps({"id":id, "yes":data["yes"], "html":render_question_tree(c)}))
	except CategoryQuestion.DoesNotExist:
		return HttpResponseBadRequest(json.dumps({"reason":"Question #%d does not exist" % id}))
	except IssueCategory.DoesNotExist:
		return HttpResponseBadRequest(json.dumps({"reason":"Category %s of source %s does not exist " % (data['name'], data["source"])}))

def delete_question(request, id):
	if request.method != "POST":
		return HttpResponseNotAllowed(["POST"])
	try:
		c = CategoryQuestion.objects.get(id=id)
		c.delete_chain()
		return HttpResponse(json.dumps({"id":id, "html":render_question_tree(None)}))
	except CategoryQuestion.DoesNotExist:
		return HttpResponseBadRequest(json.dumps({"reason":"Question #%d does not exist" % id}))

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
			print "fetching parent"
			p = CategoryQuestion.objects.get(id=parsed["parent"])
			if parsed["yes"]:
				print "setting yes on parent"
				p.set_yes(q)
				assert p.get_yes() == q, "Yes not set correctly"
			else:
				p.set_no(q)
			p.save()
			response["parent"] = p.id
			response["yes"] = parsed["yes"]

		return HttpResponse(json.dumps(response))
	else:
		return HttpResponseNotAllowed(["POST"])