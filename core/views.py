import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import BenefitsType, InformationDocuments, RequiredDocuments, Benefit, Requirement, RequirementsValue, BenefitRequrements

@csrf_exempt
def getBenefitList(request):

    if (request.method != "POST"):
        return JsonResponse (
            {
                'status': False,
                'comment': 'Неподдерживаемый метод запроса'
            }
        )


    benefit_types = BenefitsType.objects.all()

    json_data = {"data": []}

    index = 0

    for benefit_type in benefit_types:
        benefits = Benefit.objects.filter(group=benefit_type)

        if (len(json_data["data"]) <= index):
            json_data["data"].append({
                "name": benefit_type.title,
                "type": "section",
                "child": []
            })

        print(len(json_data["data"]))

        for benefit in benefits:
            json_data["data"][index]["child"].append({
                "name": benefit.title,
                "type": "item",
                "value": benefit.value,
                "detail_url": "http://127.0.0.1:8000/get-benefit-list/" + str(benefit.id),
            })

        index += 1

    return JsonResponse(json_data, safe=False, json_dumps_params={'ensure_ascii': False})



@csrf_exempt
def getBenefitById(request, id):

    if (request.method != "POST"):
        return JsonResponse (
            {
                'status': False,
                'comment': 'Неподдерживаемый метод запроса'
            }
        )

    benefit = Benefit.objects.get(id=id)

    docs = []
    for doument in benefit.information_documents.all():
        docs.append({
            "name": document.title,
            "url": document.link,
        })


    json_data = {
        "data": {
            "name": benefit.title,
            "description": benefit.description,
            "periodicity": benefit.periodicity,
            "value": benefit.value,
            "type": benefit.type,
            "start_date": benefit.start_date,
            "end_date": benefit.end_date,
            "docs": docs
        }
    }


    return JsonResponse(json_data, safe=False, json_dumps_params={'ensure_ascii': False})
