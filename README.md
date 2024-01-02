
# WHGG

League of legends Analysis Backend using Django Rest Framework.

This API allows users to get information about their League of Legends matches, including statistics, match histories and real-time game insights.

## Features

* Summoner profile data
* Match History
* Match Details
* Ranked Stats
* Champion Stats

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/Diegowh/whgg.git
```

2. Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

3. To run this project, you will need to add the following environment variables to your `.env` file

*Riot API:*
`RIOT_API_KEY`

*Database config:*
`DB_NAME`
`DB_USER`
`DB_PASSWORD`
`DB_HOST`
`DB_PORT`

*Django secret key:*
`SECRET_KEY`

4.Run the application:

```bash
python manage.py runserver
```

## API Reference

### Get Summoner

```http
  GET /api/${server}/${game_name}-${tagline}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `server` | `string` | **Required**. Summoner Server |
| `game_name` | `string` | **Required**. Riot account name |
| `tagline` | `string` | **Required**. Riot account tagline |

## Contributing

All forms of collaboration are welcome! Feel free to submit a PR or message for any kind of assistance or support.
