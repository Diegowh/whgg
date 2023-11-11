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
        

async def get_last_5_match_ids(api_client, puuid, params) -> list[str]:
    try:
        match_ids: list[str] = await api_client.get_matchlist(puuid, params)
        return match_ids
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

    # Async to Sync functions
    sync_get_summoner_puuid = async_to_sync(get_summoner_puuid)
    sync_get_last_5_match_ids = async_to_sync(get_last_5_match_ids)
    
    # Match ID params
    params = {
        'start': 0,
        'count': 5,
    }
    
    summoner_name = "wallhack"
    summoner_puuid: str = sync_get_summoner_puuid(api_client, "wallhack")
    last_5_match_ids = sync_get_last_5_match_ids(api_client, summoner_puuid, params)
    match_1: str = last_5_match_ids[0]
    match_2: str = last_5_match_ids[1]
    match_3: str = last_5_match_ids[2]
    match_4: str = last_5_match_ids[3]
    match_5: str = last_5_match_ids[4]

    return render(request, 'api-client-test.html', {'summoner_name': summoner_name, 'summoner_puuid': summoner_puuid, 'match_1': match_1, 'match_2': match_2, 'match_3': match_3, 'match_4': match_4, 'match_5': match_5})