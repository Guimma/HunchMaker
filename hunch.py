import json
from decimal import Decimal
import urllib.request

ANO = "2021"
CAMPEONATO_BRASILEIRO = "30"

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
                if game_result["home_goals"] is not None:
                    num_goals += int(game_result["home_goals"]) 
                else:
                    num_goals += 1 
            elif game_result["away_team"] == team_name:
                if game_result["away_goals"] is not None:
                    num_goals += int(game_result["away_goals"]) 
                else:
                    num_goals += 1 
    return round(num_goals/num_games)


def getGoalsByTeam(team_name, round_number):
    with open("./data/teams.json", "r", encoding='utf-8') as file:
        teams = json.load(file)
        for team in teams["equipes"]:
            if team["nome-comum"] == team_name:
                if(int(round_number) <= 6):
                    return round(Decimal(team["media-gols"]))
                else:
                    return lastGamesAverage(team_name, round_number)


def calculatePoints(current_round, only_this_round):
    max_points = 0
    points = 0

    hunchs = getJsonFromFile("hunchs")
    results = getJsonFromFile("results")

    start_round = 1
    if only_this_round:
        start_round = current_round

    for round_number in range(start_round, current_round + 1):
        round_hunchs = hunchs[str(round_number)]
        round_results = results[str(round_number)]
        print(f"\n----------RESULTADOS DA RODADA {round_number}-----------")
        for game_number in range(0, len(round_results)):
            print(f"\nJOGO {game_number + 1}")
            max_points += 25
            home_goals = int(round_results[game_number]["home_goals"])
            away_goals = int(round_results[game_number]["away_goals"])
            hunch_home_goals = int(round_hunchs[game_number]["home_goals"])
            hunch_away_goals = int(round_hunchs[game_number]["away_goals"])
            if home_goals == hunch_home_goals and away_goals == hunch_away_goals:
                points += 25
                print("Acertou placar exato!")
            elif (home_goals > away_goals and hunch_home_goals > hunch_away_goals and home_goals == hunch_home_goals) or \
                 (away_goals > home_goals and hunch_away_goals > hunch_home_goals and away_goals == hunch_away_goals):
                points += 18
                print("Acertou gols do time vencedor!")
            elif home_goals - away_goals == hunch_home_goals - hunch_away_goals:
                points += 15
                print("Acertou saldo de gols da partida!")
            elif away_goals == hunch_away_goals and home_goals > away_goals:
                points += 12
                print("Acertou gols do time perdedor!")
            elif (home_goals > away_goals and hunch_home_goals > hunch_away_goals) or \
                 (home_goals < away_goals and hunch_home_goals < hunch_away_goals):
                points += 10
                print("Acertou o vencedor da partida!")
            elif hunch_home_goals == hunch_away_goals:
                points += 4
                print("Empate garantido!")
            else:
                print("Não pontuou!")

    print(f"\nVocê fez {points} pontos de {max_points} possíveis!")
    if max_points is not 0:
        print(f"Precisão de: {round((points/max_points)*100, 2)}%")


def hunch(current_round):
    hunchs = getJsonFromFile("hunchs")
    with open("./data/hunchs.json", "w", encoding='utf-8') as file:
        for round_number in range(1, current_round + 1):
            if(round_number == current_round):
                print(f"\n------------PALPITES DA RODADA {round_number}-------------")
            round_matches = []
            for match in hunchs[str(round_number)]:
                match_result = {
                    'home_team': match["home_team"],
                    'away_team': match["away_team"],
                    'home_goals': getGoalsByTeam(match["home_team"], round_number),
                    'away_goals': getGoalsByTeam(match["away_team"], round_number),
                }
                round_matches.append(match_result)
                if(round_number == current_round):
                    print(f"{match_result['home_team']} {match_result['home_goals']} X {match_result['away_goals']} {match_result['away_team']}")
            hunchs[str(round_number)] = round_matches
        json.dump(hunchs, file, ensure_ascii=False)
    return hunchs


def setupData():
    with open("./data/temp.json", "r", encoding='utf-8') as temp_file:
        template = json.load(temp_file)
    with open("./data/hunchs.json", "w", encoding='utf-8') as hunch_file:
        json.dump(template, hunch_file, ensure_ascii=False)
    with open("./data/results.json", "w", encoding='utf-8') as hunch_file:
        json.dump(template, hunch_file, ensure_ascii=False)


def setupResults():
    with open("./data/database.json", "r", encoding='utf-8') as database_file:
        data = json.load(database_file)
        results = getJsonFromFile("results")
        hunchs = getJsonFromFile("hunchs")
        for round_number in range(1, 39):
            matches_ids = data["fases"]["3275"]["jogos"]["rodada"][str(round_number)]
            for match_id in matches_ids:
                match = data["fases"]["3275"]["jogos"]["id"][match_id]
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
                hunchs[str(round_number)].append(match_result)
                if home_goals is not None and away_goals is not None:
                    results[str(round_number)].append(match_result)

        with open("./data/results.json", "w", encoding='utf-8') as results_file:
            json.dump(results, results_file, ensure_ascii=False)
        with open("./data/hunchs.json", "w", encoding='utf-8') as hunchs_file:
            json.dump(hunchs, hunchs_file, ensure_ascii=False)
    return results


def updateData():
    page = urllib.request.urlopen(f"http://jsuol.com.br/c/monaco/utils/gestor/commons.js?callback=simulador_dados_jsonp&file=commons.uol.com.br/sistemas/esporte/modalidades/futebol/campeonatos/dados/{ANO}/{CAMPEONATO_BRASILEIRO}/dados.json")
    content = page.read()
    str_content = content.decode("utf8")
    page.close()
    data = str_content[22:].replace(');', '')
    json_data = json.loads(data)
    with open("./data/database.json", "w", encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False)
    setupResults()


def main():
    setupData()
    updateData()
    print('-----------------HUNCH MAKER-----------------')
    print('[1] - Obter palpites da rodada')
    print('[2] - Calcular precisão da rodada')
    print('[3] - Calcular precisão no campeonato')
    option = input('\nSelecione sua opção: ')

    if (option not in ["1", "2", "3"]):
        print('Opção Inválida. Tente novamente.\n')
        main()
    elif (option == "1"):
        round_number = input('Número da rodada: ')
        hunch(int(round_number))
    elif (option == "2"):
        round_number = input('Número da rodada: ')
        hunch(int(round_number))
        calculatePoints(int(round_number), True)
    elif (option == "3"):
        round_number = input('Última rodada: ')
        hunch(int(round_number))
        calculatePoints(int(round_number), False)
    

if __name__ == "__main__":
    main()
