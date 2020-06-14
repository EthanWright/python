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
    # ('April Rain - April Rain', 'April Rain'),
]

remove_strings = [
    # Single Characters
    '?', '\'', '\\', '/', '"', '`', '.', '#', '*'

    # Specific Phrases
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
]

replace_chars_mapping = {
    198: 'AE',
    200: 'E', 201: 'E',
    216: 'O',
    220: 'U',
    225: 'a', 228: 'a', 229: 'a',
    230: 'ae',
    232: 'e', 233: 'e', 235: 'e',
    237: 'i', 239: 'i',
    243: 'o', 246: 'o', 248: 'o',
    251: 'u',
    770: '^',
    8210: '-',
    8211: '-',
    8710: 'A',
    10096: '(',
    10097: ')',
    12304: '(',
    12305: ')',
}

remove_char_codes = [
    176, 768, 769, 776, 1770, 1771, 1776, 3663, 8203, 8217, 12511, 65366, 24417
]

invalid_extensions = ['jpg', 'txt', 'png', 'py', 'ini']

###################################################

improper_format_regexes = [
    '[a-zA-Z0-9](- |\()',  # `name- ` or `name(`
]
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
    '(Full Album',
    '(Full EP',
    '(The best of',
    '(Side ',
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

    '(1 and 2',
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
]