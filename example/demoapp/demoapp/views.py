import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_hoptcha.decorators import hoptcha_protected

@csrf_exempt
@hoptcha_protected(threshold=3, timeout=300, debug_ignore=True)
def protected_form_submit(request):
    try:
        data = json.loads(request.body)
        name = data.get('name', '')

        if not name:
            return JsonResponse({"error": "Name is required."}, status=400)
        return JsonResponse({"success": f"Hello, {name}!"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def form_index(request):
    return render(request, "templates/form.html")
