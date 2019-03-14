from pony.orm import *
import time

db = Database()


class Player(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    password = Required(str)
    email = Required(str)
    progress = Optional(lambda: Progress)


class Progress(db.Entity):
    id = PrimaryKey(int, auto=True)
    biggestScore = Required(int, default=0)
    gold = Required(int, default=0)
    timePlayed = Required(int, default=0)
    lastSave = Required(int, default=int(time.time()))
    player = Required(Player)
    achievements = Set('Achievement')


class Achievement(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Required(str)
    progress = Required(Progress)


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
def add_player(name, password, email):
    player = Player(name=name, password=password, email=email)
    commit()
    return player.id


@db_session
def add_progress(playerID, biggestScore, gold, timePlayed, lastSave, achievementIDs):
    player = Player.get(id=playerID)
    achievements = []
    for a in achievementIDs:
        achievements += [Achievement.get(id=a)]
    if len(achievements) == 0:
        progress = Progress(biggestScore=biggestScore, gold=gold, timePlayed=timePlayed, lastSave=lastSave,
                            player=player)
    else:
        progress = Progress(biggestScore=biggestScore, gold=gold, timePlayed=timePlayed, lastSave=lastSave,
                            player=player,
                            achievements=achievements)
    commit()
    return progress.id


@db_session
def add_achievement(name, description, progressID):
    progress = Progress.get(id=progressID)
    achievement = Achievement(name=name, description=description, progress=progress)
    commit()
    return achievement.id


@db_session
def update_player(id, name, password, email):
    player = Player.get(id=id)
    player.name = name
    player.password = password
    player.email = email
    commit()
    return player.id


@db_session
def update_progress(id, playerID, biggestScore=0, gold=0, timePlayed=0, lastSave=int(time.time()), *achievementIDs):
    player = Player.get(id=playerID)
    achievements = []
    for a in achievementIDs:
        achievements += [Achievement.get(id=a)]
    progress = Progress.get(id=id)
    progress.player = player
    progress.biggestScore = biggestScore
    progress.gold = gold
    progress.timePlayed = timePlayed
    progress.lastSave = lastSave
    progress.achievements = achievements
    commit()


@db_session
def update_achievement(id, name, description, progressID):
    progress = Progress.get(id=progressID)
    achievement = Achievement.get(id=id)
    achievement.name = name
    achievement.description = description
    achievement.progress = progress
    commit()


@db_session
def delete_player(id):
    Player[id].delete()


@db_session
def delete_progress(id):
    Progress[id].delete()


@db_session
def delete_achievement(id):
    Achievement[id].delete()


@db_session
def select_player(id):
    return Player[id]


@db_session
def select_players():
    return Player.select()[:]


@db_session
def check_player_by_name(name):
    return Player.exists(name=name)


@db_session
def select_progress_by_player(playerID):
    p = Progress.get(player=playerID)
    # return {'id': p.id,
    #         'biggestScore': p.biggestScore,
    #         'gold': p.gold,
    #         'timePlayed': p.timePlayed,
    #         'lastSave': p.lastSave,
    #         'playerId': p.player.id}
    return ProgressView(p.id, p.biggestScore, p.gold, p.timePlayed, p.lastSave, p.player)


@db_session
def select_achievement(id):
    return achievement_to_dict(Achievement[id])


@db_session
def select_achievements(progressID):
    achievements = []
    for a in Achievement.select(lambda a: a.progress.id == progressID):
        achievements += [achievement_to_dict(a)]
    return achievements


@db_session
def check_player(id):
    return Player.exists(id=id)


@db_session
def check_progress_by_player(playerID):
    return Progress.exists(player=playerID)


@db_session
def check_achievement_by_progress(progressID):
    return Achievement.exists(progress=progressID)


@db_session
def check_achievement(id):
    return Achievement.exists(id=id)


def achievement_to_dict(a):
    return {'id': a.id,
            'name': a.name,
            'description': a.description,
            }


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
if __name__ == '__main__':
    # playerID = add_player('John', 'mypass', 'john@gmail.com')
    # progressID = add_progress(playerID, 200, 2, 23)
    # add_achievement('Score above 1000', 'Ai jucat putin', progressID)
    # update_progress(5,11,2500,34,49,432423424,2)
    # delete_progress(2)
    with db_session:
        select(p for p in Player)[:].show()
        print('\n')
        select(p for p in Progress)[:].show()
        print('\n')
        select(a for a in Achievement)[:].show()
    print(select_player(1))
    print(check_player(1))
    print(select_players())
