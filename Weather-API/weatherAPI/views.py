import json
import redis

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django_ratelimit.decorators import ratelimit

from .utils.request_utils import request_api
from .utils.render_template_utils import render_template

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


@ratelimit(key="ip", rate="10/m", block=True)
def index(request):
    if request.method == "POST":
        location = request.POST["location"]

        # Check for data in the cache
        if redis_client.exists(location):
            data = redis_client.hgetall(location)
            current = json.loads(data["current"])
            hourly = json.loads(data["hourly"])
            daily = json.loads(data["daily"])
            return render_template(request, location, current, hourly, daily)

        # If there is no data in the cache, get it from the 3rd party api
        else:
            weather = request_api(location)

            if "error" in weather:
                messages.add_message(request, messages.ERROR, weather["error"])
                return HttpResponseRedirect(reverse("index"))

            else:
                current = weather["current"]
                hourly = weather["hourly"]
                daily = weather["daily"]

                # Cache
                redis_client.hset(
                    location,
                    mapping={
                        "current": json.dumps(weather["current"]),
                        "hourly": json.dumps(weather["hourly"]),
                        "daily": json.dumps(weather["daily"]),
                    },
                )
                redis_client.expire(location, 3600)
                return render_template(request, location, current, hourly, daily)

    # GET REQUEST
    else:
        return render(request, "weatherAPI/index.html", {"content": False})
