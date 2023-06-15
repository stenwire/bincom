from typing import Any

import requests
from django.db.models import Sum
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import generic
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from delta.forms import PollingUnitResultSerializer
from delta.models import AnnouncedPuResults, Lga, PollingUnit
from delta.serializers import PollingUnitResultSerializer

# from django.db.models import RawSQL


class DisplayPollingUnitResult(APIView):
    """
    Pass in the polling unit unique id to the url
    """

    renderer_classes = [TemplateHTMLRenderer]
    template_name = "polling_unit_result.html"

    def get(self, request, pk, *args, **kwargs):
        queryset = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=pk)
        return Response({"results": queryset})


def StorePollingUnitResult(request):
    if request.method == "POST":
        form = PollingUnitResultSerializer(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return HttpResponse("Result added successfully")
    else:
        form = PollingUnitResultSerializer()
    return render(request, "store_result.html", {"form": form})


def DisplayTotalPollingUnitResult(request):
    """
    query polling unit table with lga_id, pick the uniqueid
    then use the uniqueid to query announced polling unit table,
    then use a dictionary to remove duplicate,
    then sum the result
    """
    if request.method == "POST":
        selected_item = request.POST.get("selected_item")
        data = PollingUnit.objects.filter(lga_id=selected_item)
    else:
        data = PollingUnit.objects.all()

    items = Lga.objects.values_list("lga_id", flat=True)  # Get all item names

    poll_list = []
    for p in data:
        poll_list.append(p.uniqueid)

    pus_list = []
    for i in poll_list:
        pus = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=i)
        pus_list.append(pus)

    res = []
    res_dict = {}
    for j in pus_list:
        for x in j:
            res_dict[x.party_abbreviation] = x.party_score
            res.append(x.party_score)

    total = sum(res_dict.values())

    context = {
        "items": items,
        "data": res_dict,
        "total": total,
    }
    return render(request, "total_polling_unit_result.html", context)
