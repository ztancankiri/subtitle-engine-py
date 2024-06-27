import subextractor
import json
import os
from Utils import detectLanguageOfFile

dir = os.path.dirname(os.path.realpath(__file__))


def getSubtitleTrackIDsFromMKV(file):
    print(f"Retrieving subtitle track IDs of {file}")

    info = json.loads(subextractor.extract_info(file))
    tracks = list(
        filter(lambda item: item["codec_id"] == "SubRip subtitle", info))

    trackIDs = list(map(lambda item: item["index"], tracks))

    if len(trackIDs) > 0:
        print(f"Subtitle track IDs of {file} are retrieved")
    else:
        print(f"{file} does not have any subtitle tracks")

    return trackIDs


def extractSubtitleFromMKV(file, trackId, subPath):
    print(f"Extracting subtitle track {trackId} of {file}")

    result = subextractor.extract_stream(file, trackId, subPath)

    if result:
        print(f"Subtitle track {trackId} of {file} is extracted")
        return True
    else:
        print(f"Subtitle track {trackId} of {file} could not be extracted")
        return False


def extractSubtitleOfLanguageFromMKV(file, lang, subPath):
    trackIDs = getSubtitleTrackIDsFromMKV(file)

    for trackId in trackIDs:
        sub = f"{subPath}.track.{trackId}.srt"

        if extractSubtitleFromMKV(file, trackId, sub):
            if detectLanguageOfFile(sub) == lang:
                if os.path.exists(subPath):
                    os.unlink(subPath)
                os.rename(sub, subPath)
                print(f"Subtitle with lang={lang} is found and extracted")
                return True
            elif os.path.exists(sub):
                os.unlink(sub)
    print(f"Could not find the subtitle with lang={lang}")
    return False


def extractSrtByLangFromMKV(file, lang):
    videoExtName = os.path.splitext(file)[1]

    if (videoExtName == ".mkv"):
        subFile = file.replace(videoExtName, f".{lang}.srt")
        return extractSubtitleOfLanguageFromMKV(file, lang, subFile)
