# number_management_app/views.py
import json
import requests
import asyncio
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

async def fetch_data(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=0.5) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
    except asyncio.TimeoutError:
        return None
    except aiohttp.ClientError:
        return None

@csrf_exempt
@require_http_methods(["GET"])
async def get_numbers(request):
    urls = request.GET.getlist('url')
    result = {'numbers': []}

    tasks = [fetch_data(url) for url in urls]
    responses = await asyncio.gather(*tasks)

    unique_numbers = set()

    for response in responses:
        if response and isinstance(response, list):
            unique_numbers.update(response)

    result['numbers'] = sorted(list(unique_numbers))

    return JsonResponse(result)
