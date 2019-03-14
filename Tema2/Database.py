from pony.orm import *

db = Database()


class Game(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    creator = Required(str)
    description = Required(str)
    rules = Set('Rule')
    players = Set('Player')


class Player(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    password = Required(str)
    email = Required(str)
    score = Required(int)
    game = Required(Game)


class Rule(db.Entity):
    id = PrimaryKey(int, auto=True)
    description = Required(str)
    game = Required(Game)


class ProgressView:
    def __init__(self, id, biggestScore, gold, timePlayed, lastSave, player):
        self.id = id
        self.biggestScore = biggestScore
        self.gold = gold
        self.timePlayed = timePlayed
        self.lastSave = lastSave
        self.player = player


class PlayeView:
    def __init__(self, id, name, password, email):
        self.id = id
        self.name = name
        self.password = password
        self.email = email


@db_session
def add_game(name, creator, description):
    game = Game(name=name, creator=creator, description=description)
    commit()
    return game.id


@db_session
def add_rule(description, gameId):
    game = Game.get(id=gameId)
    rule = Rule(description=description, game=game)
    commit()
    return rule.id


@db_session
def add_player(name, password, email, score, gameId):
    game = Game.get(id=gameId)
    player = Player(name=name, password=password, email=email, game=game, score=score)
    commit()
    return player.id


@db_session
def update_game(id, name, creator, description):
    game = Game.get(id=id)
    game.name = name
    game.creator = creator
    game.description = description
    commit()
    return game.id


@db_session
def update_player(id, name, password, email, score, gameId):
    game = Game.get(id=gameId)
    player = Player.get(id=id)
    player.name = name
    player.password = password
    player.email = email
    player.score = score
    player.game = game
    commit()
    return player.id


@db_session
def update_rule(id, description, gameId):
    game = Game.get(id=gameId)
    rule = Rule.get(id=id)
    rule.description = description
    rule.game = game
    commit()
    return rule.id


@db_session
def delete_game(id):
    Game[id].delete()


@db_session
def delete_player(id):
    Player[id].delete()


@db_session
def delete_rule(id):
    Rule[id].delete()


@db_session
def select_game(id):
    return Game[id]


@db_session
def select_games():
    return Game.select()[:]


@db_session
def select_player(id):
    return Player[id]


@db_session
def select_players():
    return Player.select()[:]


@db_session
def select_players_by_game(gameId):
    game = Game[gameId]
    return Player.select(lambda p: p.game == game)[:]


@db_session
def select_rule(id):
    return Rule[id]


@db_session
def select_rules():
    return Rule.select()[:]


@db_session
def select_rules_by_game(gameId):
    game = Game[gameId]
    return Rule.select(lambda r: r.game == game)[:]


@db_session
def check_game(id):
    return Game.exists(id=id)


@db_session
def check_game_by_name(name):
    return Game.exists(name=name)


@db_session
def check_player_by_name(name):
    return Player.exists(name=name)


@db_session
def check_player_by_game(gameId):
    return Player.exists(game=gameId)


@db_session
def check_rule(id):
    return Rule.exists(id=id)


@db_session
def check_rule_by_game(gameId):
    return Rule.exists(game=gameId)


@db_session
def check_player(id):
    return Player.exists(id=id)


def achievement_to_dict(a):
    return {'id': a.id,
            'name': a.name,
            'description': a.description,
            }


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
if __name__ == '__main__':
    gameID1 = add_game('Snake', 'Unknown', 'oldies but goldies')
    gameID2 = add_game('Minecraft', 'Mojang', 'craft and mine')
    playerID1 = add_player('Dummy', 'parola-puternica', 'dummy@email.com', 20, gameID1)
    playerID2 = add_player('Luci', '10*4564k d', 'luci@email.com', 100, gameID1)
    add_rule('Do not hit the walls', gameID1)
    add_rule('Do not eat yourself', gameID1)
    add_rule('Do not destroy other players buildings', gameID2)
