import os
from langdetect import detect
import re
from unidecode import unidecode
import chardet

languageCodes = {
    "en": "eng",
    "tr": "tur",
    "es": "spa",
    "fr": "fra",
    "de": "deu",
    "it": "ita",
    "ja": "jpn",
    "ko": "kor",
    "zh": "zho",
    "ar": "ara",
    "ru": "rus",
    "hi": "hin",
    "pt": "por",
    "nl": "nld",
    "sv": "swe",
    "fi": "fin",
    "da": "dan",
    "no": "nor",
    "pl": "pol",
    "cs": "ces",
    "sk": "slk",
    "el": "ell",
    "he": "heb",
    "hu": "hun",
    "th": "tha",
    "vi": "vie",
    "id": "ind",
    "ms": "msa",
    "bn": "ben",
    "ur": "urd",
    "fa": "fas",
    "am": "amh",
    "sw": "swa",
    "ig": "ibo",
    "ha": "hau",
    "yor": "yor",
    "af": "afr",
    "sq": "sqi",
    "hy": "hye",
    "az": "aze",
    "eu": "eus",
    "be": "bel",
    "bs": "bos",
    "bg": "bul",
    "ca": "cat",
    "hr": "hrv",
    "eo": "epo",
    "et": "est",
    "fil": "fil",
    "gl": "glg",
    "ka": "kat",
    "gu": "guj",
    "ht": "hat",
    "haw": "haw",
    "iw": "heb",
    "hmn": "hmn",
    "hu": "hun",
    "is": "isl",
    "ig": "ibo",
    "id": "ind",
    "ga": "gle",
    "it": "ita",
    "ja": "jpn",
    "kn": "kan",
    "kk": "kaz",
    "km": "khm",
    "rw": "kin",
    "ko": "kor",
    "ku": "kur",
    "ky": "kir",
    "lo": "lao",
    "la": "lat",
    "lv": "lav",
    "lt": "lit",
    "lb": "ltz",
    "mk": "mkd",
    "mg": "mlg",
    "ms": "msa",
    "ml": "mal",
    "mt": "mlt",
    "mi": "mri",
    "mr": "mar",
    "mn": "mon",
    "my": "mya",
    "ne": "nep",
    "no": "nor",
    "ps": "pus",
    "fa": "fas",
    "pl": "pol",
    "pt": "por",
    "pa": "pan",
    "ro": "ron",
    "ru": "rus",
    "sm": "smo",
    "gd": "gla",
    "sr": "srp",
    "st": "sot",
    "sn": "sna",
    "sd": "snd",
    "si": "sin",
    "sk": "slk",
    "sl": "slv",
    "so": "som",
    "es": "spa",
    "su": "sun",
    "sw": "swa",
    "sv": "swe",
    "tl": "tgl",
    "tg": "tgk",
    "ta": "tam",
    "tt": "tat",
    "te": "tel",
    "th": "tha",
    "tr": "tur",
    "tk": "tuk",
    "uk": "ukr",
    "ur": "urd",
    "ug": "uig",
    "uz": "uzb",
    "vi": "vie",
    "cy": "cym",
    "fy": "fry",
    "xh": "xho",
    "yi": "yid",
    "yo": "yor",
    "zu": "zul"
}


def detectLanguageOfFile(file):
    with open(file, "r") as f:
        return detect(f.read())


def findLocalSub(file, lang):
    videoExtName = os.path.splitext(file)[1]

    sub1 = file.replace(videoExtName, ".srt")
    sub2 = file.replace(videoExtName, f".{lang}.srt")
    sub1Exists = os.path.exists(sub1) and os.path.isfile(
        sub1) and detectLanguageOfFile(sub1) == lang
    sub2Exists = os.path.exists(sub2) and os.path.isfile(
        sub2) and detectLanguageOfFile(sub2) == lang

    if sub1Exists:
        return sub1

    if sub2Exists:
        return sub2

    return None


def checkAndFixLocalSubFileName(file, lang):
    if len(file) > 0:
        ext = f".{lang}.srt"
        if not file.endswith(ext) and file.endswith(".srt"):
            os.rename(file, file.replace(".srt", ext))
        return True
    return False


def xml_to_dict(element):
    if len(element) == 0 and element.text is not None:
        return element.text
    result = {}
    for child in element:
        child_data = xml_to_dict(child)
        if child.tag in result:
            if type(result[child.tag]) is list:
                result[child.tag].append(child_data)
            else:
                result[child.tag] = [result[child.tag], child_data]
        else:
            result[child.tag] = child_data
    return result


def normalizeText(texts):
    normalized = " ".join(texts)
    normalized = unidecode(normalized).lower()
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized


def detectEncoding(buffer):
    result = chardet.detect(buffer)

    if result['encoding'] == "UTF-8-SIG":
        return "UTF-8-BOM"
    elif result['encoding'] == "ascii":
        return "UTF-8"
    elif result['encoding'] == "Windows-1252" or result['encoding'] == "ISO-8859-1":
        return "Windows-1254"
    else:
        return result['encoding']


def convertToUTF8BOM(buffer):
    bom_prefix = b'\xef\xbb\xbf'
    targetEncoding = "utf-8"

    detectedEncoding = detectEncoding(buffer)
    if detectedEncoding == "UTF-8-BOM":
        return buffer

    content = buffer.decode(detectedEncoding)
    return bom_prefix + content.encode(targetEncoding)


def levenshteinDistance(string1, string2):
    m = len(string1)
    n = len(string2)

    matrix = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        matrix[i][0] = i

    for j in range(n + 1):
        matrix[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 1 if string1[i - 1] != string2[j - 1] else 0
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i]
                               [j - 1] + 1, matrix[i - 1][j - 1] + cost)

    return matrix[m][n]


def calculateSimilarityPercentage(string1, string2):
    distance = levenshteinDistance(string1, string2)
    max_length = max(len(string1), len(string2))
    similarity_percentage = ((max_length - distance) / max_length) * 100
    return round(similarity_percentage, 2)
