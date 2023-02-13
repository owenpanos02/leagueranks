
def account(summoner_name):
    import requests
    import json
    with open("api_key.txt", 'r') as infile:
        api_key = str(infile.readline())
    

    decode = {'I': 1, 'II': 2, 'III': 3, 'IV': 4}
    decode_roles = {'UTILITY': 'Support', 'BOTTOM': 'ADC', 'MIDDLE': 'Mid', 'JUNGLE': 'Jungle', 'TOP':'Top'}
    decode_icon = {'Support': "static/icons/support_icon.png", 'ADC': "static/icons/bot_icon.png", 'Mid': "static/icons/middle_icon.png", 'Jungle': "static/icons/jungle_icon.png", 'Top': "static/icons/top_icon.png"}
    # Retrieve Data
    link = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}"
    response = requests.get(link)
    data = response.json()
    encrypted_id = str(data['id'])
    puuid = data['puuid']
    link2 = f'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{encrypted_id}?api_key={api_key}'
    response2 = requests.get(link2)
    ranked_data = response2.json()

    # Remove all data except ranked solo/duo
    for val in ranked_data:
        if val['queueType'] != 'RANKED_SOLO_5x5':
            ranked_data.remove(val)  
        else:
            pass
        
    # Clean Data
    winrate = ranked_data[0]['wins'] / (ranked_data[0]['wins'] + ranked_data[0]['losses'])
    rank = decode[ranked_data[0]['rank']]
    matches_endpoint = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count=10&api_key={api_key}"
    matches_response = requests.get(matches_endpoint)
    matches_data = matches_response.json()
    champs = []
    roles = []
    for i in reversed(matches_data):
        match_endpoint= f"https://americas.api.riotgames.com/lol/match/v5/matches/{i}?api_key={api_key}"
        match_response = requests.get(match_endpoint)
        match_data = match_response.json()
        for i in match_data['info']['participants']:
            if i['summonerName'] == summoner_name:
                champs.append(i['championName'])
                role = decode_roles[i['teamPosition']]
                roles.append(role)
                pass

    most_played = max(set(champs), key=champs.count)
    recent_role = max(set(roles), key=roles.count)
    role_icon = decode_icon[recent_role]

    user_info = [ranked_data[0]['summonerName'],ranked_data[0]['tier'],rank, ranked_data[0]['leaguePoints'], 'LP', f"{winrate * 100:.2f}%", most_played, recent_role, role_icon]
    return(user_info)