from datetime import datetime, UTC, timedelta
import jwt
from functools import wraps
from django.http import JsonResponse
from django.conf import settings
from ..models import User


# token required decorator
def token_required(view_func):
    @wraps(view_func)
    def decorated(request, *args, **kwargs):
        authorization_header = request.META.get("HTTP_AUTHORIZATION")
        token = authorization_header[7:]

        if not token:
            return JsonResponse({"error": "token is missing"}, status=401)

        try:
            data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            current_user = User.objects.get(id=data["id"])

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "token expired"}, status=401)

        except jwt.DecodeError:
            return JsonResponse({"error": "token invalid"}, status=401)

        except User.DoesNotExist:
            return JsonResponse({"error": "token invalid"}, status=401)

        except Exception as error:
            return JsonResponse({"error": error}, status=401)

        return view_func(request, current_user, *args, **kwargs)

    return decorated


def generate_token(user):
    return jwt.encode(
        {
            "id": user.id,
            "exp": datetime.now(UTC) + timedelta(minutes=30),
        },
        settings.SECRET_KEY,
    )
