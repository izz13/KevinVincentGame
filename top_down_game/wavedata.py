import classes, mods

wave1 = [
    ["bandit", -529, -358 + 640],
    ["bandit", -529, -496 + 640],
    ["bandit", 1563, -568 + 640],
    ["bandit", 1566, -414 + 640],
]

wave2 = [
    ["bandit", 206, 1225],
    ["bandit", 270, 1234],
    ["bandit", 342, 1252],
    ["bandit", 422, 1252],
    ["bandit", 70, -647],
    ["bandit", 134, -647],
    ["bandit", 222, -638],
    ["bandit", 302, -638],
    ["fast bandit", 222, 1180],
    ["fast bandit", 310, 1180],
    ["fast bandit", 366, 1162],
    ["fast bandit", 110, -548],
    ["fast bandit", 222, -548],
    ["fast bandit", 302, -530],
]

wave3 = [
    ["fast bandit", -97, -603],
    ["fast bandit", 52, -603],
    ["fast bandit", 216, -612],
    ["fast bandit", 396, -612],
    ["fast bandit", 690, -612],
    ["fast bandit", 1548, -188],
    ["fast bandit", 1537, -12],
    ["fast bandit", 1552, 204],
    ["fast bandit", 1548, 398],
    ["fast bandit", 1568, 618],
    ["fast bandit", 1360, 1306],
    ["fast bandit", 1086, 1306],
    ["fast bandit", 827, 1306],
    ["fast bandit", 561, 1306],
    ["fast bandit", 40, 1306],
    ["fast bandit", -583, 989],
    ["fast bandit", -599, 349],
    ["fast bandit", -607, 67],
    ["fast bandit", -607, -175],
    ["fast bandit", -595, 729],
]

waves = [wave1, wave2, wave3]

for i in range(len(waves)):
    for n in range(len(waves[i])):
        waves[i][n] = {
            "bandit" : classes.Enemy(waves[i][n][1], waves[i][n][2], 60, 90, "enemy_bandit.png", hp=400, spd=150, dmg=6, atkspd=3, cost=5),
            "fast bandit": classes.Enemy(waves[i][n][1], waves[i][n][2], 60, 90, "fastbandit.png", hp=250, spd=250, dmg=4, atkspd=6, cost=6),
             }[waves[i][n][0]]


def summon(wavenum):
    enemies = []
    currentwave = waves[wavenum]
    for enemy in currentwave:
        enemies.append(enemy)
    return enemies