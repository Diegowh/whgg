from django.shortcuts import render
from django.http import HttpResponse
from .api.api_client import ApiClient
from dotenv import dotenv_values
from asgiref.sync import async_to_sync


def requests_log(url, status, headers):
    print(url)
    print(status)
    print(headers)

async def get_summoner_puuid(api_client, name) -> str:
    try:
        data = await api_client.get_summoner_by_name(name)
        return data['puuid']
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

    sync_get_summoner_puuid = async_to_sync(get_summoner_puuid)
    summoner_name = "wallhack"
    summoner_puuid: str = sync_get_summoner_puuid(api_client, "wallhack")
    match_1: str = ""
    match_2: str = ""
    match_3: str = ""
    match_4: str = ""
    match_5: str = ""

    return render(request, 'api-client-test.html', {'summoner_name': summoner_name, 'summoner_puuid': summoner_puuid, 'match_1': match_1, 'match_2': match_2, 'match_3': match_3, 'match_4': match_4, 'match_5': match_5})