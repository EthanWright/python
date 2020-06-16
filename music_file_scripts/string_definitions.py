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
    (' - - ', ' - '),
    # ('(A)', 'A'),
]

remove_chars = [
    '?', '\'', '\\', '/', '"', '`', '.', '#', '*'
]

remove_phrases = [
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
    'Post rock and Post metal Compilation - ',
    'Post Rock Mix - ',
    'Psybient Greatest Anthems All Time Mix - ',
    'A Thousand Arms -',
    'Best Of Post Rock - ',
    'Black Hill and heklAa - ',
    'Alienation (Synthwave - ',
    'Below The Frost Line - ',
    'Post-Whatever Russia Mixtape Vol 1 (Collaboration with 9eCn3) - ',
]

remove_strings = remove_chars + remove_phrases

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
    337: 'o',
    770: '^',
    8210: '-', 8211: '-', 8212: '-',
    8226: 'and',
    8710: 'A',
    10096: '(', 10097: ')', 12304: '(', 12305: ')',
}

remove_char_codes = [
    176, 768, 769, 776, 1770, 1771, 1776, 3663, 8203, 8217, 8220, 8221, 12511, 24417, 65366,
]

#####################################################################################################

improper_format_regexes = [
    '[a-zA-Z0-9](- |\()',  # `name- ` or `name(`
]

#####################################################################################################

# Find parts of the title that potentially should be removed
potential_problem_regexes = [
    '(\[[^\]]*\])',  # [string]
    '(\([^\)]*\))',  # (string)
    '- ([01]?[0-9]) ',  # (1 ) / (01 ) / (15 ) / etc
    '\)( 20[12][0-9])',
]
acceptable_regexes = [
    '([rR][eE]?)?[mM][iI]?[xX][\)\]]',  # Remix) or Mix)  # TODO Test that this works
    # '[rR]e?mi?x[\)\]]',  # Remix)
    # '[mM]ix[\)\]]',  # Mix)
    '[\(\[][fF](ea)?[tT]',  # (Feat or (Ft
    '[vV]ersion[\)\]]',  # Version)
    ' [vV][sS] '  # TLC vs The XX
]
acceptable_phrases = [
    'Acoustic)',
    'Instrumental)',
    'Cover)',
    'Mashup)',
    'Theme)',
    'Edit)',
    'Dirty)',
    'Flip)',
    'Fix)',
    'Theme)',
    'Live)',
    'Explicit)',
    'Japanese)',
    'Refix)',
    'EP)',
    '(Full Album',
    '(The best of',
    '(Side ',
    '(Part',
    '(with ',
    '(Inspired by',  # lol

    #  Specific songs
    '(III)',
    'to gold)',
    'Breathe in)',
    'Hit Rewind)',
    'Everything is Everything)',
    'Everything Oscillates)',
    'they are everyone)',

    # '3',
    '17',
    '(1 and 2)',
    '(3)',
    '(4)',
    '(5)',
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
]
