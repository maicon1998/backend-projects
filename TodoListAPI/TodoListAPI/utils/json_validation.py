import json
from django.http import JsonResponse


def validate_json(request, required_fields):
    try:
        data = json.loads(request.body)

    # invalid json format
    except json.JSONDecodeError:
        return None, JsonResponse({"error": "Invalid JSON"}, status=400)

    else:
        # empty fields
        missing_fields = [field for field in required_fields if data.get(field) is None]
        if missing_fields:
            return None, JsonResponse(
                {"error": f"{', '.join(missing_fields)} are required"},
                status=400,
            )

        # json data
        else:
            return data, None
