from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseBadRequest,
    HttpResponseNotAllowed
)
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from templatetags.issues import render_question_tree
from django.contrib import messages
from models import (
    IssueSource,
    CategoryQuestion,
    IssueCategory,
    Issue
)
from django.core.exceptions import PermissionDenied
import json


# Convenience functions / decorators
def can_add(*models):
    """
    Decorator that makes sure users have the "add" permission for the specified models
    """
    def deco(f):
        """
        To take arguments in a decorator, we have to wrap it again
        """
        @login_required
        def wrapper(request, *args, **kwargs):
            for m in models:
                if request.user.has_perm("issues.add_%s" % m) is False:
                    raise PermissionDenied
            return f(request, *args, **kwargs)
        return wrapper
    return deco


def can_edit(*models):
    """
    Decorator that makes sure users have the "change" permission for the specified models
    """
    def deco(f):
        """
        To take arguments in a decorator, we have to wrap it again
        """
        @login_required
        def wrapper(request, *args, **kwargs):
            for m in models:
                if request.user.has_perm("issues.change_%s" % m) is False:
                    raise PermissionDenied
            return f(request, *args, **kwargs)
        return wrapper
    return deco


def can_remove(*models):
    """
    Decorator that makes sure users have the "delete" permission for the specified models
    """
    def deco(f):
        """
        To take arguments in a decorator, we have to wrap it again
        """
        @login_required
        def wrapper(request, *args, **kwargs):
            for m in models:
                if request.user.has_perm("issues.delete_%s" % m) is False:
                    raise PermissionDenied
            return f(request, *args, **kwargs)
        return wrapper
    return deco


def expects_json(f):
    """
    Decorator that parses HTTP body and passes it in as a kwarg (json_data=)
    """
    def wrapper(request, *args, **kwargs):
        if request.META.get("CONTENT_TYPE", None) == "application/json":
            data = request.body
            try:
                data = json.loads(data)
            except ValueError:
                data = None
            kwargs["json_data"] = data
        return f(request, *args, **kwargs)
    return wrapper


def json_error(message):
    """
    Convenience function for error messages on AJAX
    """
    return HttpResponseBadRequest(
        json.dumps({"reason": message})
    )


def post_only(f):
    """
    Decorator that ensures access to an endpoint is only with POST
    Since POST is used to create/delete/update data, anything
    that is POST only should be login_required.
    """
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.method != "POST":
            return HttpResponseNotAllowed(["POST"])
        else:
            return f(request, *args, **kwargs)
    return wrapper


def render_template(request, template, context):
    """
    Convenience function for automating template rendering
    Should be extracted into something we all can use...
    """
    template = loader.get_template(template)
    context = RequestContext(request, context)
    return template.render(context)


# Actual views
@login_required
@can_add("issue")
def issue_form(request):
    """
    Renders the form for submitting new issues
    """
    questions = CategoryQuestion.objects.all()
    roots = [q for q in questions if q.is_root()]
    return HttpResponse(render_template(request, "issues/issue.html",
                        {"root_questions": roots}))


@post_only
@can_add("issue")
def make_issue(request):
    c_id = request.POST["category"]
    title = request.POST["summary"]
    body = request.POST["question_text"]

    category = IssueCategory.objects.get(id=c_id)
    source = category.source

    issue = source.submit_issue(category, title, body)

    issue.subscribe(request.user)

    issue.save()

    messages.success(request, "Created issue and subscribed you to notifications for it.")

    return HttpResponseRedirect(reverse(issue_form))


@login_required
def manage_subscriptions(request):
    return HttpResponse(render_template(request, "issues/subscriptions.html", {}))


@post_only
@expects_json
def remove_subscription(request, json_data=None):
    user = request.user

    try:
        sub = user.issue_set.get(id=json_data["subscription"])
        user.issue_set.remove(sub)
        user.save()
        return HttpResponse(json.dumps({"id": json_data["subscription"]}))
    except Issue.DoesNotExist:
        return json_error("No subscription to issue %d found" % json_data["subscription"])


def get_next(request, id):
    """
    Fetches the next question in the sequence,
    based on the "yes" parameter in the query string
    and the ID of the current question.
    """
    try:
        q = CategoryQuestion.objects.get(id=id)
        data = request.GET

        if "yes" not in data:
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
            data["required_info"] = q.source.required_info

        return HttpResponse(json.dumps(data))

    except CategoryQuestion.DoesNotExist:
        return json_error("Question %d does not exist" % id)
    except AttributeError:
        yesno = "yes" if request.GET["yes"] else "no"
        return json_error("Question %d has no %s value" % (int(id), yesno))


@can_add("categoryquestion")
@can_edit("categoryquestion")
def show_question(request, source):
    """
    Displays the question-builder
    """

    s = IssueSource.objects.get(name__iexact=source)
    # Root question of every group of categories has no "no" value.
    questions = s.categoryquestion_set.all()
    roots = []
    for q in questions:
        if q.is_root():
            roots.append(q)
    return HttpResponse(
        render_template(
            request,
            "issues/questions.html",
            {"source": s, "root_questions": roots}
        ))


@post_only
@can_edit("categoryquestion")
def add_category_to_question(request, id):
    try:
        q = CategoryQuestion.objects.get(id=id)

        data = json.loads(request.body)

        if data["name"] is None:
            c = None
        else:
            c = IssueCategory.objects.get(
                name=data["name"], source__name=data["source"])

        if data["yes"]:
            q.set_yes(c)
        else:
            q.set_no(c)
        q.save()
        response = {
            "id": id,
            "yes": data["yes"],
            "html": render_question_tree(c)
        }
        return HttpResponse(json.dumps(response))
    except CategoryQuestion.DoesNotExist:
        return json_error("Question #%d does not exist" % id)
    except IssueCategory.DoesNotExist:
        return json_error("Category %s of source %s does not exist " %
                          (data['name'], data["source"]))


@post_only
@can_remove("categoryquestion")
def delete_question(request, id):
    try:
        c = CategoryQuestion.objects.get(id=id)
        c.delete_chain()
        response = {"id": id, "html": render_question_tree(None)}
        return HttpResponse(json.dumps(response))
    except CategoryQuestion.DoesNotExist:
        return json_error("Question #%d does not exist" % id)


@post_only
@expects_json
@can_add("categoryquestion")
def create_question(request, json_data=None):
    if json_data is None:
        return json_error("No data provided for new question.")
    if "text" not in json_data:
        return json_error("No text provided for question")

    text = json_data["text"]

    q = CategoryQuestion(question=text)
    if "source" in json_data:
        source = IssueSource.objects.get(name=json_data["source"])
        q.source = source
    q.save()
    response = {}
    if "parent" in json_data:
        try:
            p = CategoryQuestion.objects.get(id=int(json_data["parent"]))
            if json_data["yes"]:
                p.set_yes(q)
            else:
                p.set_no(q)
            p.save()
            response["parent"] = p.id
            response["yes"] = json_data["yes"]
        except CategoryQuestion.DoesNotExist:
            return json_error("Question %d does not exist" % json_data["parent"])

    response["id"] = q.id,
    response["question"] = q.question,
    response["html"] = render_question_tree(q)
    return HttpResponse(json.dumps(response))
