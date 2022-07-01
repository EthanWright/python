"""
String and character definitions for renaming song files

Ethan Wright - 6/10/20
"""


# TODO New file for str_constants
# class StrConstants(object):
#     SPACED_HYPHEN = ' - '
# from string_constants.StrConstants import SPACED_HYPHEN
SPACED_HYPHEN = ' - '


class CharacterCodes(object):
    replace_chars_mapping = {
        171: '(', 187: ')',
        192: 'A', 193: 'A', 194: 'A', 195: 'A', 196: 'A', 197: 'A',
        198: 'AE',
        199: 'C',
        200: 'E', 201: 'E', 202: 'E', 203: 'E',
        204: 'I', 205: 'I', 206: 'I', 207: 'I',
        208: 'D',
        209: 'N',
        210: 'O', 211: 'O', 212: 'O', 213: 'O', 214: 'O', 216: 'O',
        217: 'U', 218: 'U', 219: 'U', 220: 'U',
        221: 'Y',
        224: 'a', 225: 'a', 226: 'a', 227: 'a', 228: 'a', 229: 'a',
        230: 'ae',
        231: 'c',
        232: 'e', 233: 'e', 234: 'e', 235: 'e',
        236: 'i', 237: 'i', 238: 'i', 239: 'i',
        241: 'n',
        240: 'o', 242: 'o', 243: 'o', 244: 'o', 245: 'o', 246: 'o', 248: 'o',
        249: 'u', 250: 'u', 251: 'u', 252: 'u',
        253: 'y',
        254: 'p',
        255: 'y',

        # Extended Set
        256: 'A', 257: 'a', 258: 'A', 259: 'a', 260: 'A', 261: 'a',
        262: 'C', 263: 'c', 264: 'C', 265: 'c', 266: 'C', 267: 'c', 268: 'C', 269: 'c',
        270: 'D', 271: 'd', 272: 'D', 273: 'd',
        274: 'E', 275: 'e', 276: 'E', 277: 'e', 278: 'E', 279: 'e', 280: 'E', 281: 'e', 282: 'E', 283: 'e',
        284: 'G', 285: 'g', 286: 'G', 287: 'g', 288: 'G', 289: 'g', 290: 'G', 291: 'g',
        292: 'H', 293: 'h', 294: 'H', 295: 'h',
        296: 'I', 297: 'i', 298: 'I', 299: 'i', 300: 'I', 301: 'i', 302: 'I', 303: 'i', 304: 'I', 305: 'i',
        306: 'IJ', 307: 'ij',
        308: 'J', 309: 'j',
        310: 'K', 311: 'k', 312: 'k',
        313: 'L', 314: 'l', 315: 'L', 316: 'l', 317: 'L', 318: 'l', 319: 'L', 320: 'l', 321: 'L', 322: 'l',
        323: 'N', 324: 'n', 325: 'N', 326: 'n', 327: 'N', 328: 'n', 329: 'n', 330: 'N', 331: 'n',
        332: 'O', 333: 'o', 334: 'O', 335: 'o', 336: 'O', 337: 'o',
        338: 'OE', 339: 'oe',
        340: 'R', 341: 'r', 342: 'R', 343: 'r', 344: 'R', 345: 'r',
        346: 'S', 347: 's', 348: 'S', 349: 's', 350: 'S', 351: 's', 352: 'S', 353: 's',
        354: 'T', 355: 't', 356: 'T', 357: 't', 358: 'T', 359: 't',
        360: 'U', 361: 'u', 362: 'U', 363: 'u', 364: 'U', 365: 'u', 366: 'U', 367: 'u', 368: 'U', 369: 'u', 370: 'U', 371: 'u',
        372: 'W', 373: 'w',
        374: 'Y', 375: 'y', 376: 'Y',
        377: 'Z', 378: 'z', 379: 'Z', 380: 'z', 381: 'Z', 382: 'z',

        536: 'S', 537: 's',
        538: 'T', 539: 't',
        770: '^',
        7768: 'R',
        8210: '-', 8211: '-', 8212: '-',
        8226: 'and',
        8322: '2',
        8710: 'A',
        9658: '-',
        10096: '(', 10097: ')', 12304: '(', 12305: ')',
    }

    remove_char_codes = [
        176, 180, 768, 769, 776, 778, 1770, 1771, 1776, 3663, 8203, 8217, 8220, 8221, 8230, 8967, 9679, 9734, 12511,
        20043, 20126, 21021, 21629, 22659, 22799, 22818, 23487, 24417, 24792, 26164, 28023, 29983, 33995, 38395, 65366,
    ]

#####################################################################################################
# TODO Create classes for string formatting constants


replace_strings = [
    ('&', 'and'),
    (' _ ', ' '),
    ('.0', '_0'),
    ('[', '('),
    (']', ')'),
    ('}', ')'),
    ('{', '('),
    ('  ', ' '),
    # ('$', 'S'),  # TODO
    (' x ', ' and '),
    # (',', ' and'),  # TODO
    (',', ''),  # TODO
    (' - - ', SPACED_HYPHEN),

]

remove_chars = [
    '?', '\'', '\\', '/', '"', '`', '.', '#', '*', '!'
]

remove_phrases = [
    'added_metadata_',
    'Melodic Dubstep',
    'MrSuicideSheep',
    'Ophelia Records',
    'lyrics',
    'Lyrics',
    # 'HD',
    # 'HQ',
    # 'The Best of ',
    # 'video',
    # 'Video',
    # 'Official',
    # 'Dubstep ',
    # 'DnB ',
]
remove_strings = remove_chars + remove_phrases

# required_strings_songs_only = [
required_strings = [
    SPACED_HYPHEN,
]

improper_format_regexes = [
    r'[a-zA-Z0-9](- |\()',  # `name- ` or `name(`
    r'\)( 20[12][0-9])',
]
# improper_format_regexes_songs_only = [
#     r'^Post',
# ]

# Which one is right? Keep '()' vs trim '()' ?
parenthetical_regex = r'([\[\(][^\)\]]*[\)\]])'  # (string) or [string]
# parenthetical_regex = r'[\[\(]([^\)\]]*)[\)\]]'  # (string) or [string]

# parenthetical_regex = [
#     r'(\[[^\]]*\])',  # [string]
#     r'(\([^\)]*\))',  # (string)
# ]

# Find parts of the title that potentially should be removed
potential_problem_regexes = [
    # r'- ([01]?[0-9]) [^0-9]',  # 01 / 12 / etc
    r'- (0[0-9]|1[0-4]) [^0-9]',  # 01 / 12 / etc
    # TODO Simplify these
    r'\)( 20[012][0-9])',  # ') 2020'
    r'\((20[012][0-9] )',  # '(2020 '
    # r'( 20[012][0-9])\)',  # ' 2020)'
]
# acceptable_regexes = [
#     r'([rR][eE]?)?[mM][iI]?[xX][\)\]]',  # Remix) or Mix)
#     # r'[rR]e?mi?x[\)\]]',  # Remix)
#     # r'[mM]ix[\)\]]',  # Mix)
#     r'[\(\[][fF](ea)?[tT]',  # (Feat or (Ft
#     r'[vV]ersion[\)\]]',  # Version)
# ]

#####################################################################################################
# TODO Create classes for parenthetical value handling constants

song_version_descriptors = [
    'Acoustic',
    'Electric',
    'Instrumental',
    'Remastered',
    'Japanese',
    'Dirty',
    'Explicit',
    'Full Band',
]
song_version_suffix = [
    'Version',
    'Cover',
    'Mix',
    'Remix',
    'Refix',
    'Redux',
    'Edit',
    'Fix',
    'Flip',
    'Mashup',
    'Session',
]
song_version_prefix = [
    'Live',
    'Part',
    'Pt',
    'Volume',
    'Rehearsal',
    'Original',
]
song_version = song_version_descriptors + song_version_suffix + song_version_prefix

song_info_suffix = [
    'Theme',
]
song_info_prefix = [
    'Feat',
    'Ft',
    'EP',
    'Side ',
    'with ',
    'Full EP',
    'Full Album',
    'Album',
    'Compilation',
    'Best of',
    'Theme',
    'The best of',
    'Inspired by',
    'Collaboration',
    'Intermission',
    'Mixtape',
    'Dialogue',
    'Special Guest',
    'improvisation',
    'Intro',
    'Outro',
    'Prod by',
    'Trimmed',
    'Louder',
    'Clip',
    'Demo',
]
song_info = song_info_prefix + song_info_suffix

#  Specific songs
acceptable_song_specific_parenthetical_phrases = [
    'r',
    's',
    're',
    'lat',
    'ion',
    'fade',
    'OMSQ',
    'Mars',
    'Land',
    'hello',
    'Stage',
    'Solar',
    'Lunar',
    'Bones',
    'Ocean',
    'Think',
    'Dreams',
    'Moving',
    'purpose',
    'Theories',
    'Question',
    'You Will',
    'New Born',
    'Black Sky',
    'Waking Up',
    'Belgrade90',
    'Vinyl Play',
    'Redemption',
    'Red Moscow',
    'being born',
    'Free flight',
    'Light of Day',
    '259 Days Far',
    'The Deep Pt 1',
    'Dark of Night',
    'Second Chance',
    'While Im Away',
    'the eye of god',
    'Temple Keepers',
    'beautiful days',
    'Together We Go',
    'Sleep Paralysis',
    'The Ash of Ruin',
    'No Turning Back',
    'The sea of rains',
    'Cracked Delusion',
    'Black Heart Queen',
    '440612-N 1214609-W',
    'a Multitude of Sins',
    'The End Of Violence',
    'Projected Perfection',
    'til it turns to gold',
    '44 0612-N 121 4609-W',
    'The Decline Of Reason',
    'We Must Move Forwards',
    'The System Of Meaning',
    '01 06 1948-16 06 1987',
    'The Language Of Ghosts',
    'Trails of the Winter Storm',
    'pg lost and Wang Wen Split',
    'Are Those Who Are Forgotten',
    'question of time and distance',
    'entre la razon y el sentimiento',
    'Split with Tangled Thoughts of Leaving',

    'y',
    't',
    'me',
    'pre',
    'Red',
    'Hoi',
    'DDR',
    'etaM',
    'Dive',
    'Where',
    'I Wish',
    'Equinox',
    'Taranta',
    'Psalm 23',
    'Na Na Na',
    'Da Ba Dee',
    'Power Out',
    'The Mover',
    'FULL Flex',
    'Cable Car',
    'Birds Fly',
    'Black Flag',
    'Water Disc',
    'Long Drive',
    'The Shaker',
    'The Roller',
    'Anjunadeep',
    'For a Film',
    'Turn It In',
    'Forest Fire',
    'Till I Come',
    'Erase Traces',
    'Of The Heart',
    'Get You Dead',
    'Nobody Knows',
    'Chairman Hahn',
    'Tu Jesty Fata',
    'Everything is',
    'The Energizer',
    'I Miss Carpaty',
    'from SpongeBob',
    'I Like it Loud',
    'Falling in Love',
    'Friends Forever',
    'This Shit Rules',
    'State of Emotion',
    'Among The Living',
    'DAYS like NIGHTS',
    'Leading Us Along',
    'Beneath the Stars',
    'Daredevil Tribute',
    'The Great Illusion',
    'Come back to Texas',
    'can you see me now',
    'Intents Theme 2013',
    'My Sweet Roisin Dubh',
    'Bordello Kind Of Guy',
    'Costumes For Tonight',
    'Where Sea Meets Shore',
    'Slishal No Ne Zapisal',
    'You Do It To Yourself',
    'Songs From Japanese Anime',
    'Variations on a Shaker Hymn',
    'Heart Comes Out Of My Chest',
    'Balkan Express Train Robbery',
    'That Which Cannot Be Created',
    'A tribute To Ralph Serravalle',
    'Hopping On A Pogo-Gypsy Stick',
    'Light and Day Reach For The Sun',

    'dj stories',
    'WSN Club Dub',
    'Autumn Chills',
    'TLC vs The XX',
    'Apocalyptic Mix by Das Ich',
    'BBC 1Xtra - Mistajam Daily Does',
    'Zeds Dead VIP Remix Ft Omar LinX',

    '3',
    '4',
    '5',
    'III',
    '1453',
    '1and2',
    '1 and 2',
    'Nexus pt 1',
    'Nexus pt 2',
    'Existing I',
    'Existing II',
    'Existing III',
    'Existing IV',
    'Existence I',
    'Existence II',
    'Existence III',
    'Existence IV',
    'The Lighthouse Symphony Pt3',
    'The Lighthouse Symphony Pt2',

]
