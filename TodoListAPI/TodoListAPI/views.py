from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

from .utils.json_validation import validate_json
from .models import User, Todos
from .utils.token_manager import generate_token, token_required


@csrf_exempt
def register(request):
    if request.method == "POST":
        data, error = validate_json(request, ["name", "email", "password"])

        # invalid json format or empty fields
        if error:
            return error

        else:
            name = data["name"]
            email = data["email"]
            password = data["password"]

            try:
                user = User.objects.create_user(name, email, password)
                user.save()
                token = generate_token(user)
                return JsonResponse({"token": token}, status=201)

            except IntegrityError:
                return JsonResponse({"error": "Email already taken."}, status=422)

    # POST method only
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def login(request):
    if request.method == "POST":
        data, error = validate_json(request, ["email", "password"])

        # invalid json format or empty fields
        if error:
            return error

        else:
            email = data["email"]
            password = data["password"]
            User = get_user_model()

            try:
                user = User.objects.get(email=email)

                if user.check_password(password):
                    token = generate_token(user)
                    return JsonResponse({"token": token}, status=201)

                else:
                    return JsonResponse(
                        {"error": "Invalid email and/or password"}, status=401
                    )

            except User.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=404)

    # POST method only
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@token_required
def todos_create_read(request, current_user):
    if request.method == "POST":
        data, error = validate_json(request, ["title", "description"])

        # invalid json format or empty fields
        if error:
            return error

        else:
            title = data["title"]
            description = data["description"]

            # create a to-do item
            try:
                Todos.objects.create(
                    author=current_user, title=title, description=description
                )
                return JsonResponse(data, status=201)

            except Exception as error:
                return JsonResponse({"error": error}, status=400)

    elif request.method == "GET":
        # pagination
        todos = Todos.objects.filter(author=current_user)
        limit = request.GET.get("limit")
        paginator = Paginator(todos, limit)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        data = [
            {"id": todo.id, "title": todo.title, "description": todo.description}
            for todo in page_obj
        ]

        return JsonResponse(
            {
                "data": data,
                "page": int(page_number),
                "limit": int(limit),
                "total": paginator.count,
            },
            safe=False,
            status=200,
        )

    # POST and GET methods only
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@token_required
def todos_update_delete(request, current_user, id):
    if request.method == "PUT":
        data, error = validate_json(request, ["title", "description"])

        # invalid json format or empty fields
        if error:
            return error

        else:
            try:
                todo = Todos.objects.get(id=id)
            except Todos.DoesNotExist:
                return JsonResponse({"error": "Todo not found"}, status=404)

            # only the to-do author can update it
            if todo.author == current_user:
                title = data["title"]
                description = data["description"]

                # update the to-do item
                try:
                    todo.title = title
                    todo.description = description
                    todo.save()

                    return JsonResponse(
                        {"title": todo.title, "description": todo.description},
                        status=200,
                    )

                except Exception as error:
                    return JsonResponse({"error": error}, status=400)

            # cannot update the to-do of others
            else:
                return JsonResponse({"error": "Forbidden"}, status=403)

    elif request.method == "DELETE":
        try:
            todo = Todos.objects.get(id=id)
        except Todos.DoesNotExist:
            return JsonResponse({"error": "Todo not found"}, status=404)

        # only the to-do author can delete it
        if todo.author == current_user:
            try:
                todo.delete()

                return JsonResponse(
                    {"message": "Todo deleted successfully"}, status=204
                )

            except Exception as error:
                return JsonResponse({"error": error}, status=400)

        # cannot delete the to-do of others
        else:
            return JsonResponse({"error": "Forbidden"}, status=403)

    # PUT and DELETE methods only
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
