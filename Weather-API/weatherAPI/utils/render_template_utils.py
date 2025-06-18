from django.shortcuts import render


def render_template(request, location, current, hourly, daily):
    return render(
        request,
        "weatherAPI/index.html",
        {
            "city": location,
            "current": current,
            "hourly": zip(
                hourly["time"],
                hourly["temperature_2m"],
                hourly["precipitation_probability"],
            ),
            "daily": zip(
                daily["time"],
                daily["temperature_2m_max"],
                daily["temperature_2m_min"],
                daily["precipitation_probability_max"],
            ),
        },
    )
