config = {
# ----- Game setup ---------------------------------------------------
    'paths' : {
        'images' : 'Images',
        'fonts' : 'Fonts',
        'modules' : 'Games',
        'music' : 'Music',
        'sounds' : 'Sounds',
    },
    'screen' : {
        # screen size
        'size' : (158, 260),
        # name : (file name, colorkey)
        'icon' : ('icon.bmp', None),
        'image' : ('_screen_.png', 0x00ff00),
    },
    'fonts': {
        # name : (filename, width, height, colorkey, additional chars)
        'ta_font' : ('_font1_.png', 11, 15, 0x00ff00, 1),
        'disp_font' : ('_font2_.png', 10, 10, 0x00ff00, 25),
        # font backgroung must be 0x000000,
    },
# ----- UI components setup ------------------------------------------
    'textareas' : {
        # name : (position, size in chars, text color, font name)
        'main' : ((2, 231), (14, 1), 0x00ff00, 'ta_font'),
        'score' : ((65, 5), (8, 1), 0x00ff00, 'ta_font'),
        'speed' : ((121, 92), (2, 1), 0x00ff00, 'ta_font'),
        'level' : ((121, 118), (2, 1), 0x00ff00, 'ta_font'),
    },
    'displays' : {
        # name : (position, size in chars, default color, layers, font index)
        'main' : ((6, 24), (10, 20), 0x00ff00, 3, 'disp_font'),
        'lives' : ((110, 40), (4, 4), 0x00ff00, 2, 'disp_font'),
        'extra' : ((110, 194), (4, 3), 0x00ff00, 2, 'disp_font'),
    },
    'indicators' : {
        # background color when indicator turned off
        'bg_color' : 0x2a2a2a,
        # name, color, rect
        'score': (0x00ff00, (34, 5, 29, 7)),
        'hiscore' : (0xff0000, (8, 5, 55, 7)),
        'lines' : (0x00ff00, (36, 14, 27, 7)),
        'pause' : (0x00ff00, (116, 179, 31, 9)),
        'rotate' : (0x00ff00, (114, 136, 35, 7)),
        'r1' : (0x00ff00, (128, 147, 4, 8)),
        'r2' : (0x00ff00, (133, 145, 4, 8)),
        'gameA' : (0x00ff00, (116, 158, 31, 7)),
        'gameB' : (0x00ff00, (116, 167, 31, 7)),
        'sound' : (0x00ff00, (6, 14, 7, 7)),
        's1' : (0x00ff00, (15, 14, 3, 7)),
        's2' : (0x00ff00, (20, 14, 5, 7)),
        's3' : (0x00ff00, (27, 14, 4, 7)),
        'next' : (0x00ff00, (114, 23, 23, 7)),
        'lives' : (0x00ff00, (114, 32, 27, 7)),
        'speed' : (0x00ff00, (117, 84, 29, 7)),
        'level' : (0x00ff00, (117, 110, 29, 7)),
    }
}

# Additional info
# colorkey - None or RGB value
# filename - Only file name (without folder names like 'Images')