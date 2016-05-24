# -*- coding: utf-8 -*-

import re
import unicodedata

SCHOOL_TYPES = [
    'academy',
    'alternative',
    'art',
    'collegiate',
    'combined',
    'comprehensive',
    'day',
    'free',
    'grammar',
    'high',
    'higher',
    'independent',
    'infant',
    'infants',
    'international',
    'islamic',
    'jewish',
    'junior',
    'language',
    'media',
    'middle',
    'montessori',
    'nursery',
    'pre',
    'prep',
    'preparatory',
    'primary',
    'secondary',
    'senior'
    'special',
    'specialist',
    'temple',
    ]

STOP_WORDS = [
    'a',
    'aided',
    'al',
    'all',
    'and',
    'at',
    'baptist',
    'boys',
    'british',
    'building',
    'by',
    'catholic',
    'central',
    'children',
    'christ',
    'christian',
    'church',
    'class',
    'cofe',
    'college',
    'common',
    'community',
    'controlled',
    'dame',
    'de',
    'education',
    'educational',
    'end',
    'england',
    'english',
    'for',
    'form',
    'fro',
    'further',
    'g',
    'girls',
    'gymraeg',
    'heath',
    'hill',
    'i',
    'in',
    'independent',
    'le',
    'learning',
    'london',
    'long',
    'methodist',
    'mixed',
    'more',
    'needs',
    'o',
    'of',
    'old',
    'on',
    'our',
    'pupil',
    'r',
    'rc',
    'referral',
    'resource',
    'roman',
    'royal',
    's',
    'sacred',
    'saint',
    'saints',
    'school',
    'schools',
    'services',
    'shcool',
    'short',
    'sir',
    'sixth',
    'st',
    'th',
    'the',
    'va',
    'vc',
    'vi',
    'voluntary',
    'years',
    'ysgol',
    ]


def deaccent(text):
    """
    Remove accentuation from the given string. Input text is either a unicode string or utf8 encoded bytestring.
    Return input string with accents removed, as unicode.
    >>> deaccent("Šéf chomutovských komunistů dostal poštou bílý prášek")
    u'Sef chomutovskych komunistu dostal postou bily prasek'
    """
    norm = unicodedata.normalize("NFD", text)
    result = u''.join(ch for ch in norm if unicodedata.category(ch) != 'Mn')
    return unicodedata.normalize("NFC", result)

PAT_ALPHABETIC = re.compile('(((?![\d])\w)+)', re.UNICODE)

def tokenize(text, lowercase=True, deacc=True, errors="strict"):
    """
    Iteratively yield tokens as unicode strings, removing accent marks
    and optionally lowercasing the unidoce string by assigning True
    to one of the parameters, lowercase, to_lower, or lower.
    Input text may be either unicode or utf8-encoded byte string.
    The tokens on output are maximal contiguous sequences of alphabetic
    characters (no digits!).
    >>> list(tokenize('Nic nemůže letět rychlostí vyšší, než 300 tisíc kilometrů za sekundu!', deacc = True))
    [u'Nic', u'nemuze', u'letet', u'rychlosti', u'vyssi', u'nez', u'tisic', u'kilometru', u'za', u'sekundu']
    """
    if text:
        if lowercase:
            text = text.lower()
        if deacc:
            text = deaccent(text)
        for match in PAT_ALPHABETIC.finditer(text):
            yield match.group()
