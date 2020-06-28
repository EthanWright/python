"""
String and character definitions for renaming song files

Ethan Wright - 6/10/20
"""

replace_strings = [
    ('&', 'and'),
    (' _ ', ' '),
    ('.0', '_0'),
    ('[', '('),  # TODO
    (']', ')'),  # TODO
    ('  ', ' '),
    # ('$', 'S'),  # TODO
    (' x ', ' and '),
    # (',', ' and'),  # TODO
    (',', ''),  # TODO
    (' - - ', ' - '),
]

remove_chars = [
    '?', '\'', '\\', '/', '"', '`', '.', '#', '*'
]

remove_phrases = [
    'added_metadata_',
    'Melodic Dubstep',
    'MrSuicideSheep',
    'lyrics',
    'Lyrics',
    'video',
    'Video',
    'HD',
    'HQ',
    # 'Official',
    # 'Dubstep ',
    # 'DnB ',
]
remove_strings = remove_chars + remove_phrases

# Songs Only
remove_phrases_songs_only = [
    'Post Rock',
    'Post Rock Mix',
    'Post Rock Hungary',
    'Post Rock Australia',
    'Post Rock_Metal_Experimental Austria',
    'Post Rock_Metal_Experimental Italy',
    'Post Rock and Post metal Compilation',
    'Post-Whatever Russia Mixtape Vol 1 (Collaboration with 9eCn3)',
    'Post-Whatever Switzerland',
    'Post-Whatever India',
    'Post-Whatever Russia',
    'Post-Whatever Belgium',
    'Post Music Spain Mixtape',
    'Best Of Post Rock',
    'A Thousand Arms',
    'Below The Frost Line',
    'Black Hill and heklAa',
    'Alienation (Synthwave',
    'Psybient Greatest Anthems All Time Mix',
    'WPRDs Top 30 Post-Rock_Metal_Experimental Songs of 2017 (Part 2)',
]

#####################################################################################################

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

    536: 'S',
    770: '^',
    7768: 'R',
    8210: '-', 8211: '-', 8212: '-',
    8226: 'and',
    8710: 'A',
    10096: '(', 10097: ')', 12304: '(', 12305: ')',


}

remove_char_codes = [
    176, 768, 769, 776, 778, 1770, 1771, 1776, 3663, 8203, 8217, 8220, 8221, 8230, 12511,
    20043, 20126, 21021, 21629, 22659, 22799, 22818, 23487, 24417, 26164, 28023, 29983, 33995, 65366,
]

#####################################################################################################

improper_format_regexes = [
    r'[a-zA-Z0-9](- |\()',  # `name- ` or `name(`
    r'- ([01]?[0-9]) ',  # (1 ) / (01 ) / (15 ) / etc
    r'\)( 20[12][0-9])',
]
improper_format_regexes_songs_only = [
    r'^Post',
]
required_strings = []
required_strings_songs_only = [
    r' - ',
]

#####################################################################################################

parentheses_regex = r'([\[\(][^\)\]]*[\)\]])'  # (string) or  [string]
# parentheses_regexes = [
#     r'(\[[^\]]*\])',  # [string]
#     r'(\([^\)]*\))',  # (string)
# ]

# Find parts of the title that potentially should be removed
potential_problem_regexes = [
    r'- ([01]?[0-9]) [^0-9]',  # 01 / 15 / etc
    # r'\)( 20[12][0-9])',
]
# acceptable_regexes = [
#     r'([rR][eE]?)?[mM][iI]?[xX][\)\]]',  # Remix) or Mix)
#     # r'[rR]e?mi?x[\)\]]',  # Remix)
#     # r'[mM]ix[\)\]]',  # Mix)
#     r'[\(\[][fF](ea)?[tT]',  # (Feat or (Ft
#     r'[vV]ersion[\)\]]',  # Version)
#     r' [vV][sS] '  # TLC vs The XX
# ]
song_version = [
    'Acoustic',
    'Cover',
    'Dirty',
    'Edit',
    'Explicit',
    'Fix',
    'Flip',
    'Instrumental',
    'Japanese',
    'Live',
    'Mashup',
    'Refix',
    'Remastered',
    'Remix',
    'Version',
]
song_details = [
    'Feat',
    'Ft',
    'Theme',
    'EP',
    'Full Album',
    'Best of',
    'The best of',
    'Side ',
    'Part',
    'with ',
    'Inspired by',
    'Collaboration',
    'Intermission',
    # 'Release',
    'Dialogue',
    'Intro',
    'Outro',
    'Special Guest',
]
acceptable_phrases = song_version + song_details

#  Specific songs
acceptable_phrases_song_specific = [
    '(r)',
    '(re)',
    '(lat)',
    '(OMSQ)',
    '(hello)',
    '(Mars)',
    '(Stage)',
    '(Theories)',
    '(Bones)',
    '(Ocean)',
    '(Question)',
    '(Land)',
    '(Think)',
    '(Moving)',
    '(Black Sky)',
    '(Temple Keepers)',
    '(Second Chance)',
    '(New Born)',
    '(Sleep Paralysis)',
    '(The Ash of Ruin)',
    '(The Last Dawn)',
    '(Hymn to the Immortal Wind)',
    '(Walking Cloud and Deep Red Sky Flag Fluttered and the Sun Shined)',
    '(Requiem for Hell)',
    '(You Are There)',
    '(For My Parents)',
    '(Rays of Darkness)',
    '(Trails of the Winter Storm)',
    '(One Step More and Youll Die)',
    '(beautiful days)',
    '(Together We Go)',
    '(259 Days Far)',
    '(We Must Move Forwards)',
    '(No Turning Back)',
    '(Free flight)',
    '(The sea of rains)',
    '(Red Moscow)',
    '(question of time and distance)',
    '(Waking Up)',
    '(the eye of god)',
    '(44 0612-N 121 4609-W)',
    '(Belgrade90)',
    '(Black Heart Queen)',
    '(Are Those Who Are Forgotten)',
    '(While Im Away)',
    '(The End Of Violence)',
    '(The Language Of Ghosts)',
    '(The Decline Of Reason)',
    '(The System Of Meaning)',
    '(til it turns to gold)',
    '(1 and 2)',
    '(3)',
    '(4)',
    '(5)',
    '(III)',
    '(Existing IV)',
    '(Existing III)',
    '(Existing II)',
    '(Existing I)',
    '(Existence IV)',
    '(Existence III)',
    '(Existence II)',
    '(Existence I)',
    '(Nexus pt 2)',
    '(Nexus pt 1)',

]
# TODO Handle this via cli args
RENAMING_SONGS = True
# RENAMING_SONGS = False

# Add SONGS ONLY lists
if RENAMING_SONGS:
    remove_strings += remove_phrases_songs_only
    required_strings += required_strings_songs_only
    acceptable_phrases += acceptable_phrases_song_specific
    improper_format_regexes += improper_format_regexes_songs_only