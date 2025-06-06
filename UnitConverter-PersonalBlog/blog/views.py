from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .models import User, Articles
from .util import articles, new_edit_article, error_message


def redirect(request):
    return HttpResponseRedirect(reverse("blog:login"))


@login_required
def home(request):
    return render(request, "blog/home.html", {"articles": articles(request)})


@login_required
def article(request, id):
    article = Articles.objects.filter(id=id).values("title", "published", "content")
    return render(request, "blog/article.html", {"article": article})


@login_required
def admin(request):
    article = articles(request)

    if request.method == "POST":
        article_id = request.POST["article-id"]

        # for delete validation
        article_author = Articles.objects.filter(id=article_id).values("author")

        # Prevent a user from deleting another user's article by changing the article_id in the form input
        if request.user.id == article_author[0]["author"]:
            try:
                Articles.objects.get(id=article_id).delete()
                return HttpResponseRedirect(reverse("blog:admin"))
            except Exception as error:
                print(error)
                error_message(request, "Error when deleting the article")
                return HttpResponseRedirect(reverse("blog:admin"))

        # if a user changes the article_id to a non-existent one
        else:
            error_message(request, "Error when deleting the article")
            return HttpResponseRedirect(reverse("blog:admin"))

    # GET REQUEST
    else:
        return render(request, "blog/admin.html", {"articles": article})


@login_required
def new(request):
    if request.method == "POST":
        fields = new_edit_article(request)

        if type(fields) is dict:
            Articles(
                author=request.user,
                published=fields["date"],
                title=fields["title"],
                content=fields["content"],
            ).save()
            return HttpResponseRedirect(reverse("blog:home"))
        else:
            error_message(request, fields)
            return HttpResponseRedirect(reverse("blog:new"))

    # GET REQUEST
    else:
        return render(request, "blog/new.html")


@login_required
def edit(request, id):
    article = Articles.objects.filter(id=id).values("title", "content")

    if request.method == "POST":
        fields = new_edit_article(request)

        if type(fields) is dict:
            Articles.objects.filter(author=request.user, id=id).update(
                title=fields["title"],
                published=fields["date"],
                content=fields["content"],
            )
            return HttpResponseRedirect(reverse("blog:home"))

        else:
            error_message(request, fields)
            return HttpResponseRedirect(reverse("blog:edit"))

    # GET REQUEST
    else:
        return render(
            request,
            "blog/edit.html",
            {"title": article[0]["title"], "content": article[0]["content"]},
        )


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except IntegrityError:
            error_message(request, "Username already exists")
            return HttpResponseRedirect(reverse("blog:register"))

        return HttpResponseRedirect(reverse("blog:login"))

    # GET REQUEST
    else:
        return render(request, "blog/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("blog:home"))
        else:
            error_message(request, "Invalid username and/or password.")
            return HttpResponseRedirect(reverse("blog:login"))

    else:
        return render(request, "blog/login.html")


@login_required
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Successfully logged out")
    return HttpResponseRedirect(reverse("blog:login"))
