from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .util import converter, length_converter, weight_converter, temperature_converter


def redirect(request):
    return HttpResponseRedirect(reverse("unit_converter:length"))


def length(request):
    if request.method == "POST":
        return converter(request, length_converter)
    else:
        return render(request, "unit_converter/length.html")


def weight(request):
    if request.method == "POST":
        return converter(request, weight_converter)
    else:
        return render(request, "unit_converter/weight.html")


def temperature(request):
    if request.method == "POST":
        return converter(request, temperature_converter)
    else:
        return render(request, "unit_converter/temperature.html")
