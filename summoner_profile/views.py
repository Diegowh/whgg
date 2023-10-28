from django.shortcuts import render
from django.http import HttpResponse
from .api.api_client import ApiClient
from dotenv import dotenv_values

async def test_api_client(request):
    try:
        env_vars = dotenv_values('.env')
        api_key = env_vars.get('RIOT_API_KEY')

        if api_key is None:
            raise KeyError("RIOT_API_KEY not found in the .env file")
    except KeyError as e:
        return HttpResponse(f"Error: {e}")

    server = "euw1"

    api_client = ApiClient(server=server, api_key=api_key)
    status = await api_client.get_league_pages()


    return render(request, 'api-client-test.html', {'status': status})