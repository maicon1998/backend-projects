from .models import Articles
from django.contrib import messages


def articles(request):
    return (
        Articles.objects.filter(author=request.user)
        .values("id", "author", "title", "published")
        .order_by("-published")
    )


def new_edit_article(request):
    title = request.POST.get("title", None)
    date = request.POST.get("date", None)
    content = request.POST.get("content", None)

    if title is None:
        return "Title required"
    elif date is None:
        return "Date required"
    elif content is None:
        return "Content required"
    else:
        return {"title": title, "date": date, "content": content}


def error_message(request, message):
    return messages.add_message(request, messages.ERROR, message)
