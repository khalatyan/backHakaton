import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import BenefitsType, InformationDocuments, RequiredDocuments, Benefit, Requirement, RequirementsValue, BenefitRequrements, BenefitsGroup

@csrf_exempt
def getBenefitList(request):

    if (request.method != "POST"):
        return JsonResponse (
            {
                'status': False,
                'comment': 'Неподдерживаемый метод запроса'
            }
        )


    benefit_groups = BenefitsGroup.objects.all()

    json_data = {"data": []}

    index = 0

    for benefit_group in benefit_groups:
        benefits = Benefit.objects.filter(group=benefit_group)

        if (len(json_data["data"]) <= index):
            json_data["data"].append({
                "name": benefit_group.title,
                "type": "section",
                "child": []
            })

        print(len(json_data["data"]))

        for benefit in benefits:
            json_data["data"][index]["child"].append({
                "name": benefit.title,
                "type": benefit.type.title,
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
    for document in benefit.information_documents.all():
        docs.append({
            "name": document.title,
            "url": document.link,
        })


    json_data = {
        "data": {
            "name": benefit.title,
            "description": benefit.description,
            "periodicity": benefit.periodicity.title,
            "value": benefit.value,
            "type": benefit.type.title,
            "start_date": benefit.start_date,
            "end_date": benefit.end_date,
            "docs": docs
        }
    }


    return JsonResponse(json_data, safe=False, json_dumps_params={'ensure_ascii': False})



@csrf_exempt
def getAnswer(request):

    if (request.method != "POST"):
        return JsonResponse (
            {
                'status': False,
                'comment': 'Неподдерживаемый метод запроса'
            }
        )

    request_body = json.loads( request.body.decode( 'utf-8' ) )["data"]

    json_data = {"data": []}

    benefits = Benefit.objects.all()

    for benefit in benefits:

        benefit_requirements = BenefitRequrements.objects.filter(benefit=benefit)

        status = 1

        for benefit_requirement in benefit_requirements:
            print(benefit_requirement)
            if not (benefit_requirement.requirement_value.requirement.title in request_body):
                status = 2
                break

            if (benefit_requirement.sign == 3):
                if not (request_body[benefit_requirement.requirement_value.requirement.title] == benefit_requirement.requirement_value.value):
                    status = 3
                    break
            elif(benefit_requirement.sign == 2):
                if not (request_body[benefit_requirement.requirement_value.requirement.title] <= benefit_requirement.requirement_value.value):
                    status = 3
                    break
            else:
                if not (request_body[benefit_requirement.requirement_value.requirement.title] >= benefit_requirement.requirement_value.value):
                    status = 3
                    break


        if (status == 1):
            data = {
                "name": benefit.title,
                "status": True,
                "detail_url": "http://127.0.0.1:8000/get-benefit-list/" + str(benefit.id),
            }

            json_data["data"].append(data)
        elif (status == 2):
            data = {
                "name": benefit.title,
                "status": "Недостаточно данных",
                "detail_url": "http://127.0.0.1:8000/get-benefit-list/" + str(benefit.id),
            }
            json_data["data"].append(data)


    return JsonResponse(json_data, safe=False, json_dumps_params={'ensure_ascii': False})
