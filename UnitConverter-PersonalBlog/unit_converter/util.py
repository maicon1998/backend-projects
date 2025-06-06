import json
from django.http import JsonResponse


def converter(request, converter):
    try:
        data = json.loads(request.body)
        result = converter(
            float(data.get("value")), data.get("from_unit"), data.get("to_unit")
        )
        return JsonResponse({"result": result})
    except Exception as e:
        return JsonResponse({"error": e}, status=400)


def length_converter(length, from_unit, to_unit):
    conversion = {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1,
        "km": 1000,
        "in": 0.0254,
        "ft": 0.3048,
        "yd": 0.9144,
        "mi": 1609.344,
    }

    converted = (length * conversion[from_unit]) / conversion[to_unit]
    return f"{round(converted, 3)} {to_unit}"


def weight_converter(weight, from_unit, to_unit):
    conversion = {
        "mg": 1,
        "g": 1000,
        "kg": 1000000,
        "oz": 28349.5231,
        "lbs": 453592.37,
    }
    converted = (weight * conversion[from_unit]) / conversion[to_unit]
    return f"{round(converted, 3)} {to_unit}"


def temperature_converter(length, from_unit, to_unit):
    match from_unit:
        case "celsius":
            match to_unit:
                case "celsius":
                    return f"{length}ºC"
                case "fahrenheit":
                    return f"{round((9 / 5) * length + 32, 2)}ºF"
                case "kelvin":
                    return f"{round(length + 273.15, 2)} K"

        case "fahrenheit":
            match to_unit:
                case "fahrenheit":
                    return f"{length}ºF"
                case "celsius":
                    return f"{round((5 / 9) * (length - 32), 2)}ºC"
                case "kelvin":
                    return f"{round((5 / 9) * (length - 32) + 273.15, 2)} K"

        case "kelvin":
            match to_unit:
                case "kelvin":
                    return f"{length} K"
                case "celsius":
                    return f"{round(length - 273.15, 2)}ºC"
                case "fahrenheit":
                    return f"{round((5 / 9) * (length - 273.15) + 32, 2)}ºF"
