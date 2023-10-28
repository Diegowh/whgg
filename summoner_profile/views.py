from django.shortcuts import render
from django.http import HttpResponse
from .api.api_client import ApiClient
from dotenv import dotenv_values
from asgiref.sync import async_to_sync


def requests_log(url, status, headers):
    print(url)
    print(status)
    print(headers)

async def get_summoner_id(api_client, name):
    try:
        data = await api_client.get_summoner_by_name(name)
        return (data['id'], data['accountId'])
    except Exception as e:
        print(e)

def test_api_client(request):
    try:
        env_vars = dotenv_values('.env')
        api_key = env_vars.get('RIOT_API_KEY')

        if api_key is None:
            raise KeyError("RIOT_API_KEY not found in the .env file")
    except KeyError as e:
        return HttpResponse(f"Error: {e}")

    server = "euw1"

    api_client = ApiClient(server, api_key, requests_logging_function=requests_log, debug=True)

    sync_get_summoner_id = async_to_sync(get_summoner_id)
    status = sync_get_summoner_id(api_client, "wallhack")

    return render(request, 'api-client-test.html', {'status': status})