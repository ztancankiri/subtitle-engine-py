import os
import subprocess
from Utils import detectLanguageOfFile

dir = os.path.dirname(os.path.realpath(__file__))
mkvinfo = os.path.join(dir, "mkvinfo")
mkvextract = os.path.join(dir, "mkvextract")


def getSubtitleTrackIDsFromMKV(file):
    print(f"Retrieving subtitle track IDs of {file}")

    process = subprocess.Popen(
        [mkvinfo, file], stdout=subprocess.PIPE, text=True)
    stdout, _ = process.communicate()

    trackIDs = stdout.replace("\n", "").split(
        "|+ Tracks")[1].split("| + Track")
    trackIDs = list(filter(lambda item: len(item) > 0, trackIDs))
    trackIDs = list(map(lambda item: f"SUB|{item[0]}" if (
        "Track type: subtitles" in item[1]) else item, enumerate(trackIDs)))
    trackIDs = list(filter(lambda item: "SUB|" in item, trackIDs))
    trackIDs = list(map(lambda item: int(item.split("|")[1]), trackIDs))

    if len(trackIDs) > 0:
        print(f"Subtitle track IDs of {file} are retrieved")
    else:
        print(f"{file} does not have any subtitle tracks")

    return trackIDs


def extractSubtitleFromMKV(file, trackId, subPath):
    print(f"Extracting subtitle track {trackId} of {file}")

    process = subprocess.Popen(
        [mkvextract, "tracks", file, f"{trackId}:{subPath}"], stdout=subprocess.PIPE, text=True)
    stdout, _ = process.communicate()

    if "Progress: 100%" in stdout:
        print(f"Subtitle track {trackId} of {file} is extracted")
        return True
    else:
        print(f"Subtitle track {trackId} of {file} could not be extracted")
        return False


def extractSubtitleOfLanguageFromMKV(file, lang, subPath):
    trackIDs = getSubtitleTrackIDsFromMKV(file)

    for trackId in trackIDs:
        sub = f"{subPath}.track.{trackId}"

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
