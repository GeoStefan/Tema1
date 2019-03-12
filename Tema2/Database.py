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


@db_session
def add_player(name, password, email):
    player = Player(name=name, password=password, email=email)
    commit()
    return player.id


@db_session
def add_progress(playerID, biggestScore=0, gold=0, timePlayed=0, lastSave=int(time.time()), *achievementIDs):
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
    p = Player[id]
    return export_player(p)


@db_session
def select_players():
    players = []
    for p in Player.select():
        players += [export_player(p)]
    return players


@db_session
def check_player(id):
    return Player.exists(id=id)


def export_player(p):
    return {'id': p.id,
            'name': p.name,
            'password': p.password,
            'email': p.email}


def export_progress(p):
    return {'id': p.id,
            'biggestScore': p.biggestScore,
            'gold': p.gold,
            'timePlayed': p.timePlayed,
            'lastSave': p.lastSave,
            'playerId': p.player.id}


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
