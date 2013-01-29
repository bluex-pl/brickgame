def test(screen):
    # pola tekstowe (main, score, speed, level)
    screen.textareas.main.replace('Bardzo dlugi przykladowy tekst')
    screen.textareas.score.put(123)
    screen.textareas.score.align('r0')
    screen.textareas.score.color(0xff0000)
    screen.textareas.speed.put(1)
    screen.textareas.speed.align('r0')
    screen.textareas.level.put(4)
    screen.textareas.level.align('r0')
    # kontrolki (score, hiscore, lines, pause, rotate, r1, r2, gameA, gameB,
    #            sound, s1, s2, s3, next, lives, speed, level)
    screen.indicators.hiscore.state = 1
    screen.indicators.lives.state = 1
    screen.indicators.speed.state = 1
    screen.indicators.level.state = 1
    # wyswietlacze (main, lives, extra)
    screen.displays.main.clear()
    screen.displays.main.visibility(True, [0, 2])
    screen.displays.main.fill((3,6,5,5), 0x81, 0x00ffff, 0)
    screen.displays.main.fill((0,0,3,3), 0x82, 0xff00ff, 0)
    screen.displays.main.put_text((3,10,10,4), 'tes t\nabc\n1234567890123456789', 0xffffff, 0)
    screen.displays.main.copy((1,1,3,3), (3,3), 0)
    screen.displays.main.copy((3,10,2,2), (7,5), 2, 0)
    screen.displays.main.put_text((0, 17, 5, 2), 'abcd', 0xff0000, 2)
    screen.displays.main.map_data((0, 15, 3, 5), imgs.digits[0], layer=0)
    screen.displays.main.fill((0, 17, 10, 3), 0x82, 0xffffff, 2)
    screen.displays.lives.clear()
    screen.displays.lives.visibility(True, 1)
    screen.displays.lives.fill((0,0,5,5), 0x81, 0x00ffff)
    screen.displays.extra.clear()
    screen.displays.extra.visibility(True)
    screen.displays.extra.fill((0, 0, 4, 3), 0x83, 0xffaa00)
    screen.displays.extra.map_data((0, 0, 4, 3),((0x8E,0x8B,0x8B,0x8F),(0x8A,None,None,0x8A),(0x8C,0x8B,0x8B,0x8D)))