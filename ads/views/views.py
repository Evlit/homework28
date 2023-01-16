from django.http import JsonResponse


def index(request):
    if request.method == "GET":
        response = {"status": "ok"}
        return JsonResponse(response, safe=False)
