import json
from decimal import Decimal
# pegar os jogos da rodada
# criar json com os resultados da rodada
# criar json com os palpites da rodada
# criar cálculo de quantos pontos fiz / pontos possíveis

def getJsonFromFile(path):
    with open(f"./data/{path}.json", "r", encoding='utf-8') as file:
        return json.load(file)

def getTeamById(id):
    with open("./data/teams.json", "r", encoding='utf-8') as file:
        teams = json.load(file)
        for team in teams["equipes"]:
            if team["id"] == id:
                return team

def lastGamesAverage(team_name, round_number):
    num_games = int(round_number)
    num_goals = 0
    results = getJsonFromFile("results")
    for round_number in range(1,num_games):
        for game_number in range(0, 10):
            game_result = results[str(round_number)][game_number]
            if game_result["home_team"] == team_name:
                num_goals += int(game_result["home_goals"]) 
            elif game_result["away_team"] == team_name:
                num_goals += int(game_result["away_goals"]) 
    return round(num_goals/num_games)

def getGoalsByTeam(team_name, round_number):
    with open("./data/teams.json", "r", encoding='utf-8') as file:
        teams = json.load(file)
        for team in teams["equipes"]:
            if team["nome-comum"] == team_name:
                if(int(round_number) <= 5):
                    return round(Decimal(team["media-gols"]))
                else:
                    return lastGamesAverage(team_name, round_number)

def calculatePoints(hunchs, results):
    max_points = 0
    points = 0

    for round_number in range(1, 39):
        round_hunchs = hunchs[str(round_number)]
        round_results = results[str(round_number)]
        print(f"\nRODADA {round_number}")
        for game_number in range(0, 10):
            print(f"\nJOGO {game_number + 1}")
            max_points += 25
            home_goals = int(round_results[game_number]["home_goals"])
            away_goals = int(round_results[game_number]["away_goals"])
            hunch_home_goals = int(round_hunchs[game_number]["home_goals"])
            hunch_away_goals = int(round_hunchs[game_number]["away_goals"])
            if home_goals == hunch_home_goals and away_goals == hunch_away_goals:
                points += 25
                print("Acertou placar exato!")
            elif home_goals == hunch_home_goals and home_goals > away_goals:
                points += 18
                print("Acertou gols do time vencedor!")
            elif home_goals - away_goals == hunch_home_goals - hunch_away_goals:
                points += 15
                print("Acertou saldo de gols da partida!")
            elif away_goals == hunch_away_goals and home_goals > away_goals:
                points += 12
                print("Acertou gols do time perdedor!")
            elif home_goals > away_goals and hunch_home_goals > hunch_away_goals or \
                 home_goals < away_goals and hunch_home_goals < hunch_away_goals:
                points += 10
                print("Acertou o vencedor da partida!")
            elif hunch_home_goals == hunch_away_goals:
                points += 4
                print("Empate garantido!")

    print(f"\nVocê fez {points} pontos de {max_points} possíveis!")
    print(f"Precisão de: {round((points/max_points)*100, 2)}%")

def hunch():
    hunchs = getJsonFromFile("hunchs")
    results = getJsonFromFile("results")
    with open("./data/hunchs.json", "w", encoding='utf-8') as file:
        for round_number in results:
            round_matches = []
            for match in results[round_number]:
                match_result = {
                    'home_team': match["home_team"],
                    'away_team': match["away_team"],
                    'home_goals': getGoalsByTeam(match["home_team"], round_number),
                    'away_goals': getGoalsByTeam(match["away_team"], round_number),
                }
                round_matches.append(match_result)
            hunchs[str(round_number)] = round_matches
        json.dump(hunchs, file, ensure_ascii=False)
    print("Palpites gerados!")
    return hunchs

def setupResults():
    with open("./data/raw_2020.json", "r", encoding='utf-8') as file:
        data = json.load(file)
        results = getJsonFromFile("results")
        for round_number in range(1, 39):
            matches_ids = data["fases"]["3062"]["jogos"]["rodada"][str(round_number)]
            for match_id in matches_ids:
                match = data["fases"]["3062"]["jogos"]["id"][match_id]
                home_team = getTeamById(match["time1"])
                away_team = getTeamById(match["time2"])
                home_goals = match["placar1"]
                away_goals = match["placar2"]
                match_result = {
                    'home_team': home_team["nome-comum"],
                    'away_team': away_team["nome-comum"],
                    'home_goals': home_goals,
                    'away_goals': away_goals,
                }
                results[str(round_number)].append(match_result)
        with open("./data/results.json", "w", encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False)
    print("Resultados obtidos!")
    return results

def main():
    results = getJsonFromFile("results")
    if (not results["1"]):
        results = setupResults()
    hunchs = hunch()
    calculatePoints(hunchs, results)
    

if __name__ == "__main__":
    main()
