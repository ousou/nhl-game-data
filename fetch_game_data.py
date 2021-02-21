import urllib.request, urllib.error
import json
import os
import gzip
import concurrent.futures

stats_api_live_url = "https://statsapi.web.nhl.com/api/v1/game/%s/feed/live"
data_folder = "data"
game_types = {
    "preseason": 1,
    "regular": 2,
    "playoffs": 3,
    "allstar": 4
}


def game_count(season):
    if season >= 2017:
        return 1271
    else:
        return 1230


def create_game_id(season, game_type, game_id):
    return str(season) + str(game_type).zfill(2) + str(game_id).zfill(4)


def fetch_full_game_data(season, game_type, game_id):
    url = stats_api_live_url % create_game_id(season, game_type, game_id)

    with urllib.request.urlopen(url) as u:
        return game_id, json.loads(u.read().decode())


def fetch_and_store_all_regular_season_data_for_season(season):
    print("Fetching game data for season %i" % season)
    season_data_folder = data_folder + "/" + str(season)
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    if not os.path.exists(season_data_folder):
        os.makedirs(season_data_folder)

    game_type = game_types["regular"]
    games_fetched = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(lambda game_id: fetch_full_game_data(
            season,
            game_type,
            game_id
        ), range(1, game_count(season) + 1))
        for game_id, game_data in results:
            if game_id % 10 == 0:
                print("Fetching data for game_id %i" % game_id)
            file_name = "%s.json.gz" % game_id
            with gzip.open(season_data_folder + "/" + file_name, "w") as f:
                f.write(json.dumps(game_data).encode("utf-8"))
            games_fetched += 1

    if games_fetched == game_count(season):
        print("Game data fetched for season %i for all %i games" % (season, game_count(season)))
    else:
        print("ERROR! Could fetch data for season %i only for %i of %i games" %
              (season, games_fetched, game_count(season)))

if __name__ == '__main__':
    fetch_and_store_all_regular_season_data_for_season(2017)