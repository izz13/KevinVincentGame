import classes, mods

wave0 = [
    ["bandit", -529, -358 + 640],
    ["bandit", -529, -496 + 640],
    ["bandit", 1563, -568 + 640],
    ["bandit", 1566, -414 + 640],
]


waves = [wave0]

for i in range(len(waves)):
    for n in range(len(waves[i])):
        waves[i][n] = {
            "bandit" : classes.Enemy(waves[i][n][1], waves[i][n][2], 60, 90, "enemy_bandit.png", hp=200, spd=150, dmg=6, atkspd=3, cost=5),
             }[waves[i][n][0]]


def summon(wavenum):
    enemies = []
    currentwave = waves[wavenum]
    for enemy in currentwave:
        enemies.append(enemy)
    return enemies