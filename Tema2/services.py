import Database
import re
import time


def get_games():
    games = []
    gg = Database.select_games()
    for g in gg:
        games += [game_to_dict(g)]
    return (200, games)


def get_game(id):
    if Database.check_game(id):
        return (200, game_to_dict(Database.select_game(id)))
    else:
        return (404, 'Game not found')


def post_game(game):
    keys = ['name', 'description', 'creator']
    for k in keys:
        if k not in game.keys():
            return (400, k + ' key not found in request')
    if not isinstance(game['name'], str):
        return (400, 'Invalid type for name key')
    if not isinstance(game['description'], str):
        return (400, 'Invalid type for description key')
    if not isinstance(game['creator'], str):
        return (400, 'Invalid type for creator key')
    if not re.match('^\w+$', game['name']):
        return (422, 'Invalid name, name should contain only characters')
    if Database.check_game_by_name(game['name']):
        return (409, 'Game with same name already exists')
    else:
        id = Database.add_game(game['name'], game['creator'], game['description'])
        return (201, id)


def put_game(game, id):
    keys = ['name', 'description', 'creator']
    for k in keys:
        if k not in game.keys():
            return (400, k + ' key not found in request')
    if not isinstance(game['name'], str):
        return (400, 'Invalid type for name key')
    if not isinstance(game['description'], str):
        return (400, 'Invalid type for description key')
    if not isinstance(game['creator'], str):
        return (400, 'Invalid type for creator key')
    if not re.match('^\w+$', game['name']):
        return (422, 'Invalid name, name should contain only characters')
    if not Database.check_game_by_name(game['name']):
        return (404, 'Game not found')
    else:
        id = Database.update_game(id, game['name'], game['creator'], game['description'])
        return (200, id)


def delete_game(id):
    if not Database.check_game(id):
        return (404, 'Game not found')
    Database.delete_game(id)
    return (204, None)


def get_player(id):
    if Database.check_player(id):
        return (200, player_to_dict(Database.select_player(id)))
    else:
        return (404, 'Player not found')


def get_players():
    players = []
    pp = Database.select_players()
    for p in pp:
        players += [player_to_dict(p)]
    return (200, players)


# def get_progress(playerID):
#     if Database.check_progress_by_player(playerID):
#         progress = Database.select_progress_by_player(playerID)
#         achievements = Database.select_achievements(progress.id)
#         return progress_to_dict(progress, achievements)
#     else:
#         return None
#
#
# def get_achievements(playerID):
#     progress = get_progress(playerID)
#     if progress != None:
#         return progress['achievements']
#     else:
#         return None
#
#
# def get_achievement(id, playerID):
#     progress = get_progress(playerID)
#     if progress != None:
#         achievements = progress['achievements']
#         if len(achievements) > 0:
#             achievement = Database.select_achievement(id)
#             if achievement in achievements:
#                 return achievement
#     return None


def post_player(player):
    keys = ['name', 'password', 'email', 'score', 'gameId']
    for k in keys:
        if k not in player.keys():
            return (400, k + ' key not found in request')
    if not isinstance(player['name'], str):
        return (400, 'Invalid type for name key')
    if not isinstance(player['password'], str):
        return (400, 'Invalid type for password key')
    if not isinstance(player['email'], str):
        return (400, 'Invalid type for email key')
    if not isinstance(player['score'], int):
        return (400, 'Invalid type for score key')
    if not isinstance(player['gameId'], int):
        return (400, 'Invalid type for gameId key')
    if not re.match('^\w+$', player['name']):
        return (422, 'Invalid name, name should contain only characters')
    if player['score'] < 0:
        return (422, 'Invalid score')
    if Database.check_player_by_name(player['name']):
        return (409, 'Player name already exists')
    if not Database.check_game(int(player['gameId'])):
        return (422, 'Invalid gameId: gameId does not exist')
    id = Database.add_player(player['name'], player['password'], player['email'], player['score'], player['gameId'])
    return (201, {'id': id})


def put_player(player, id):
    keys = ['name', 'password', 'email']
    for k in keys:
        if k not in player.keys():
            return (400, k + ' key not found in request')
    if not isinstance(player['name'], str):
        return (400, 'Invalid type for name key')
    if not isinstance(player['password'], str):
        return (400, 'Invalid type for password key')
    if not isinstance(player['email'], str):
        return (400, 'Invalid type for email key')
    if not re.match('^\w+$', player['name']):
        return (422, 'Invalid name, name should contain only characters')
    if not Database.check_player(id):
        return (404, 'Player not found')
    id = Database.update_player(id, player['name'], player['password'], player['email'], player['score'],
                                player['gameId'])
    return (200, {'id': id})


def delete_player(id):
    if not Database.check_player(id):
        return (404, 'Player not found')
    Database.delete_player(id)
    return (204, None)


def get_rules():
    rules = []
    rr = Database.select_rules()
    for r in rr:
        rules += [rule_to_dict(r)]
    return (200, rules)


def get_rule(id):
    if Database.check_rule(id):
        return (200, rule_to_dict(Database.select_rule(id)))
    else:
        return (404, 'Rule not found')


def post_rule(rule):
    keys = ['description', 'gameId']
    for k in keys:
        if k not in rule.keys():
            return (400, k + ' key not found in request')
    if not isinstance(rule['description'], str):
        return (400, 'Invalid type for description key')
    if not isinstance(rule['gameId'], int):
        return (400, 'Invalid type for gameId key')
    if not Database.check_game(int(rule['gameId'])):
        return (422, 'Invalid gameId: gameId does not exist')
    id = Database.add_rule(rule['description'], rule['gameId'])
    return (201, {'id': id})


def put_rule(rule, id):
    keys = ['description', 'gameId']
    for k in keys:
        if k not in rule.keys():
            return (400, k + ' key not found in request')
    if not isinstance(rule['description'], str):
        return (400, 'Invalid type for description key')
    if not isinstance(rule['gameId'], int):
        return (400, 'Invalid type for gameId key')
    if not Database.check_game(int(rule['gameId'])):
        return (422, 'Invalid gameId: gameId does not exist')
    if not Database.check_rule(id):
        return (404, 'Rule not found')
    id = Database.update_rule(id, rule['description'], rule['gameId'])
    return (200, {'id': id})


def delete_rule(id):
    if not Database.check_rule(id):
        return (404, 'Rule not found')
    Database.delete_rule(id)
    return (204, None)


def get_player_by_game(gameId, playerId):
    if not Database.check_game(gameId):
        return (404, 'Game not found')
    if not Database.check_player_by_game(gameId):
        return (404, 'Player not found')
    return get_player(playerId)


def get_players_by_game(gameId):
    if not Database.check_game(gameId):
        return (404, 'Game not found')
    if not Database.check_player_by_game(gameId):
        return (204, None)
    players = []
    pp = Database.select_players_by_game(gameId)
    for p in pp:
        players += [player_to_dict(p)]
    return (200, players)


def get_rule_by_game(gameId, ruleId):
    if not Database.check_game(gameId):
        return (404, 'Game not found')
    if not Database.check_rule_by_game(gameId):
        return (404, 'Rule not found')
    return get_rule(ruleId)


def get_rules_by_game(gameId):
    if not Database.check_game(gameId):
        return (404, 'Game not found')
    if not Database.check_rule_by_game(gameId):
        return (204, None)
    rules = []
    rr = Database.select_players_by_game(gameId)
    for r in rr:
        rules += [player_to_dict(r)]
    return (200, rules)


def player_to_dict(p):
    return {'id': p.id,
            'name': p.name,
            'password': p.password,
            'email': p.email}


def game_to_dict(g):
    return {'id': g.id,
            'name': g.name,
            'creator': g.creator,
            'description': g.description}


def rule_to_dict(r):
    return {'id': r.id,
            'description': r.description}
