import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from .models import Posts


@csrf_exempt
def create_read(request):
    if request.method == "POST":
        # validate JSON data
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        title = data.get("title")
        content = data.get("content")
        category = data.get("category")
        tags = data.get("tags")

        # check for empty fields
        if None in (title, content, category, tags) or not isinstance(tags, list):
            return JsonResponse(
                {"error": "title, content, category and tags (as a list) are required"},
                status=400,
            )

        # save post
        else:
            try:
                post = Posts.objects.create(
                    title=title, content=content, category=category
                )
                post.tags.add(*tags)

            except Exception as error:
                return JsonResponse({"error": error}, status=400)

            else:
                return JsonResponse(data, status=201)

    elif request.method == "GET":
        term = request.GET.get("term", "").strip()

        # posts with the filter
        if term:
            posts = Posts.objects.filter(
                Q(title__icontains=term)
                | Q(content__icontains=term)
                | Q(category__icontains=term)
            ).prefetch_related("tags")

        # all posts
        else:
            posts = Posts.objects.prefetch_related("tags").all()

        data = [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "category": post.category,
                "createdAt": post.createdAt,
                "updatedAt": post.updatedAt,
                "tags": list(post.tags.names()),
            }
            for post in posts
        ]

        if not data:
            return JsonResponse({"error": "No posts found"}, status=404)
        else:
            return JsonResponse(data, safe=False, status=200)

    # only GET and POST are accepted
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def read_update_delete(request, id):
    if request.method == "PUT":
        # validate JSON data
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        title = data.get("title")
        content = data.get("content")
        category = data.get("category")
        tags = data.get("tags")

        # check for empty fields
        if None in (title, content, category, tags) or not isinstance(tags, list):
            return JsonResponse(
                {
                    "error": "title, content, category, and tags (as a list) are required"
                },
                status=400,
            )

        # update post
        else:
            try:
                post = Posts.objects.get(id=id)
                post.title = title
                post.content = content
                post.category = category
                post.save()
                post.tags.set(tags)

                return JsonResponse(
                    {
                        "id": post.id,
                        "title": post.title,
                        "content": post.content,
                        "category": post.category,
                        "tags": list(post.tags.names()),
                    },
                    status=200,
                )

            except Posts.DoesNotExist:
                return JsonResponse({"error": "Post not found"}, status=404)

            except Exception as error:
                return JsonResponse({"error": error}, status=400)

    elif request.method == "DELETE":
        # delete post
        try:
            post = Posts.objects.get(id=id)
            post.delete()
            return JsonResponse({"success": "Post deleted successfully"}, status=204)

        except Posts.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)

        except Exception as error:
            return JsonResponse({"error": error}, status=400)

    elif request.method == "GET":
        # get a single post
        try:
            post = Posts.objects.prefetch_related("tags").get(id=id)

            data = {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "category": post.category,
                "createdAt": post.createdAt,
                "updatedAt": post.updatedAt,
                "tags": list(post.tags.names()),
            }
            return JsonResponse(data, status=200)

        except Posts.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)

    # only PUT, DELETE and GET are accepted
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
