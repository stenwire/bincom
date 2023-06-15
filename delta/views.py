from typing import Any
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views import generic
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from delta.serializers import PollingUnitResultSerializer
from delta.forms import PollingUnitResultSerializer

# from django.db.models import RawSQL


import requests

from delta.models import AnnouncedPuResults, PollingUnit, Lga


class DisplayPollingUnitResult(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'polling_unit_result.html'

    def get(self, request, pk, *args, **kwargs):
        queryset = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=pk)
        return Response({'results': queryset})


def DisplayTotalPollingUnitResult(request, pk, *args: Any, **kwargs: Any):
        '''
        query polling unit table with lga_id, pick the uniqueid
        then use the uniqueid to query announced polling unit table the sum the result
        '''
        poll = PollingUnit.objects.filter(lga_id=pk)
        poll_list = []
        for p in poll:
            poll_list.append(p.uniqueid)

        pus_list = []
        for i in poll_list:
            pus = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=i)
            pus_list.append(pus)

        res = []
        for j in pus_list:
            for x in j:
                res.append(x.party_score)

        total = sum(res)
        print(poll_list)
        context = {
            'result': total,
        }
        return render(request, 'total_polling_unit_result.html', context)

def StorePollingUnitResult(request):
    if request.method == "POST":
        form = PollingUnitResultSerializer(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return HttpResponse('Result added successfully')
    else:
        form = PollingUnitResultSerializer()
    return render(request, 'store_result.html', {'form': form})