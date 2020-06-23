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
    (',', ' and'),  # TODO
    # (',', ''),  # TODO
    (' - - ', ' - '),
    ('(Mixtape Vol 1)', '- Mixtape 1 -'),
    ('(Mixtape Vol 2)', '- Mixtape 2 -'),
    ('(Mixtape Vol 3)', '- Mixtape 3 -'),
    # ('(A)', 'A'),
]

remove_chars = [
    '?', '\'', '\\', '/', '"', '`', '.', '#', '*'
]

remove_phrases = [
    'added_metadata_',
    'Melodic Dubstep',
    'MrSuicideSheep',
    # 'Official',
    'lyrics',
    'Lyrics',
    'video',
    'Video',
    'HD',
    'HQ',
    # '(Dubstep ',
    # '(DnB ',
]
remove_strings = remove_chars + remove_phrases

# Songs Only
remove_phrases_songs_only = [
    'A Thousand Arms',
    'Below The Frost Line',
    'Best Of Post Rock',
    'Black Hill and heklAa',
    'Psybient Greatest Anthems All Time Mix',
    'Alienation (Synthwave',
    'WPRDs Top 30 Post-Rock_Metal_Experimental Songs of 2017 (Part 2)',
    'Post Music Spain Mixtape',
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
    251: 'u', 252: 'u',
    259: 'a',
    337: 'o',
    363: 'u',
    536: 'S',
    770: '^',
    7768: 'R',
    8210: '-', 8211: '-', 8212: '-',
    8226: 'and',
    8710: 'A',
    10096: '(', 10097: ')', 12304: '(', 12305: ')',
}

remove_char_codes = [
    176, 768, 769, 776, 778, 1770, 1771, 1776, 3663, 8203, 8217, 8220, 8221, 8230, 12511, 24417, 65366,
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

parentheses_regex = r'([\(\[][^\)\]]*[\(\[])'  # (string) or  [string]
# parentheses_regexes = [
#     r'(\[[^\]]*\])',  # [string]
#     r'(\([^\)]*\))',  # (string)
# ]

# Find parts of the title that potentially should be removed
# potential_problem_regexes = [
#     r'- ([01]?[0-9]) ',  # (1 ) / (01 ) / (15 ) / etc
#     r'\)( 20[12][0-9])',
# ]
# acceptable_regexes = [
#     r'([rR][eE]?)?[mM][iI]?[xX][\)\]]',  # Remix) or Mix)
#     # r'[rR]e?mi?x[\)\]]',  # Remix)
#     # r'[mM]ix[\)\]]',  # Mix)
#     r'[\(\[][fF](ea)?[tT]',  # (Feat or (Ft
#     r'[vV]ersion[\)\]]',  # Version)
#     r' [vV][sS] '  # TLC vs The XX
# ]
acceptable_phrases = [
    'Acoustic',
    'Instrumental',
    'Cover',
    'Mashup',
    'Theme',
    'Edit',
    'Dirty',
    'Flip',
    'Feat',
    'Fix',
    'Remix',
    'Theme',
    'Version',
    'Live',
    'Explicit',
    'Japanese',
    'Refix',
    'EP',
    'Full Album',
    'Best of',
    'The best of',
    'Side ',
    'Part',
    'with ',
    'Inspired by',
    'Collaboration',
    'Remastered',
    'Live',
]
#  Specific songs
acceptable_phrases_song_specific = [
    # '(3)',
    # '(4)',
    # '(5)',
    '17',
    '(III)',
    '(1 and 2)',
    '(Mars)',
    '(Black Sky)',
    '(Theories)',
    '(Bones)',
    '(Ocean)',
    '(Question)',
    '(Land)',
    '(Think)',
    '(Temple Keepers)',
    '(Second Chance)',
    '(New Born)',
    '(lat)',
    '(Sleep Paralysis)',
    '(The Ash of Ruin)',
    '(The Last Dawn)',
    '(Hymn to the Immortal Wind)',
    '(Walking Cloud and Deep Red Sky Flag Fluttered and the Sun Shined)',
    '(Requiem for Hell)',
    '(You Are There)',
    '(For My Parents)',
    '(Bonus track)',
    '(Rays of Darkness)',
    '(Trails of the Winter Storm)',
    '(One Step More and Youll Die)',
    '(beautiful days)',
    '(Together We Go)',
    '(Live At Old South Church)',
    '(r)',
    '(hello)',
    '(259 Days Far)',
    '(OMSQ)',
    '(We Must Move Forwards)',
    '(No Turning Back)',
    '(Free flight)',
    '(The sea of rains)',
    '(Red Moscow)',

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
