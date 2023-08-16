import os
from OpenSubtitles import OpenSubtitles
from SubSync import sync
from Utils import findLocalSub, checkAndFixLocalSubFileName
from MkvTools import extractSrtByLangFromMKV

from Node import Node


def checkEnSrt(file):
    sub = findLocalSub(file, "en")

    if (sub is not None):
        print(f"EN SRT FOUND: {sub}")
        return True

    print("NO EN SRT")
    return False


def checkTrSrt(file):
    sub = findLocalSub(file, "tr")

    if (sub is not None):
        print(f"TR SRT FOUND: {sub}")
        return True

    print("NO TR SRT")
    return False


def extractEnSrtFromMkv(file):
    return extractSrtByLangFromMKV(file, "en")


def extractTrSrtFromMkv(file):
    return extractSrtByLangFromMKV(file, "tr")


def getEnSrtByHash(file):
    opensub = OpenSubtitles()
    token = opensub.login()
    results = opensub.searchHash(token, "eng", file)

    if (len(results) == 0):
        print("Search Error on getEnSrtByHash")
        return False

    matches = list(filter(
        lambda item: item["SubLanguageID"] == "eng" and item["SubFormat"] == "srt", results))

    if (len(matches) == 0):
        print("No match!")
        return False

    bestMatch = matches[0]
    foundSubtitles = opensub.download(bestMatch["ZipDownloadLink"])

    if (len(foundSubtitles) > 0):
        subtitle = foundSubtitles[0]
        print(f"DOWNLOADED EN SRT BY HASH: {subtitle['name']}")
        videoExtName = os.path.splitext(file)[1]
        subtitlePath = file.replace(videoExtName, ".en.srt")
        with open(subtitlePath, "wb") as f:
            f.write(subtitle["data"])
        return True
    return False


def getTrSrtByHash(file):
    opensub = OpenSubtitles()
    token = opensub.login()
    results = opensub.searchHash(token, "tur", file)

    if (len(results) == 0):
        print("Search Error on getTrSrtByHash")
        return False

    matches = list(filter(
        lambda item: item["SubLanguageID"] == "tur" and item["SubFormat"] == "srt", results))

    if (len(matches) == 0):
        print("No match!")
        return False

    bestMatch = matches[0]
    foundSubtitles = opensub.download(bestMatch["ZipDownloadLink"])

    if (len(foundSubtitles) > 0):
        subtitle = foundSubtitles[0]
        print(f"DOWNLOADED TR SRT BY HASH: {subtitle['name']}")
        videoExtName = os.path.splitext(file)[1]
        subtitlePath = file.replace(videoExtName, ".tr.srt")
        with open(subtitlePath, "wb") as f:
            f.write(subtitle["data"])
        return True
    return False


def getEnSrtByName(file):
    opensub = OpenSubtitles()
    token = opensub.login()
    results = opensub.searchName(token, "eng", file)

    if (len(results) == 0):
        print("Search Error on getEnSrtByName")
        return False

    matches = list(filter(
        lambda item: item["SubLanguageID"] == "eng" and item["SubFormat"] == "srt", results))

    if (len(matches) == 0):
        print("No match!")
        return False

    bestMatch = matches[0]
    foundSubtitles = opensub.download(bestMatch["ZipDownloadLink"])

    if (len(foundSubtitles) > 0):
        subtitle = foundSubtitles[0]
        print(f"DOWNLOADED EN SRT BY NAME: {subtitle['name']}")
        videoExtName = os.path.splitext(file)[1]
        subtitlePath = file.replace(videoExtName, ".en.srt")
        with open(subtitlePath, "wb") as f:
            f.write(subtitle["data"])
        return True
    return False


def getTrSrtByName(file):
    opensub = OpenSubtitles()
    token = opensub.login()
    results = opensub.searchName(token, "tur", file)

    if (len(results) == 0):
        print("Search Error on getTrSrtByName")
        return False

    matches = list(filter(
        lambda item: item["SubLanguageID"] == "tur" and item["SubFormat"] == "srt", results))

    if (len(matches) == 0):
        print("No match!")
        return False

    bestMatch = matches[0]
    foundSubtitles = opensub.download(bestMatch["ZipDownloadLink"])

    if (len(foundSubtitles) > 0):
        subtitle = foundSubtitles[0]
        print(f"DOWNLOADED TR SRT BY NAME: {subtitle['name']}")
        videoExtName = os.path.splitext(file)[1]
        subtitlePath = file.replace(videoExtName, ".tr.srt")
        with open(subtitlePath, "wb") as f:
            f.write(subtitle["data"])
        return True
    return False


def subsyncTrSrtWithEnSrt(file):
    refLang = "en"
    subLang = "tr"

    refPath = findLocalSub(file, refLang)
    subPath = findLocalSub(file, subLang)

    syncedSubFile = sync(subPath, subLang, refPath, refLang)
    return checkAndFixLocalSubFileName(syncedSubFile, subLang)


def subsyncEnSrtWithAudio(file):
    refLang = "en"
    subLang = "en"

    refPath = file
    subPath = findLocalSub(file, subLang)

    syncedSubFile = sync(subPath, subLang, refPath, refLang)
    return checkAndFixLocalSubFileName(syncedSubFile, subLang)


def subsyncTrSrtWithAudio(file):
    refLang = "en"
    subLang = "tr"

    refPath = file
    subPath = findLocalSub(file, subLang)

    syncedSubFile = sync(subPath, subLang, refPath, refLang)
    return checkAndFixLocalSubFileName(syncedSubFile, subLang)


def readyEnSrt(file):
    print("Ready EN srt.")
    return True


def readyTrSrt(file):
    print("Ready TR srt.")
    return True


def readyTrSrtAndEnSrt(file):
    print("Ready All")
    return True


def readyNothing(file):
    print(":(")
    return True


def runEngine(file):
    node1 = Node(checkEnSrt, file)
    node2 = Node(getTrSrtByHash, file)
    node3 = Node(readyTrSrtAndEnSrt, file)
    node4 = Node(subsyncTrSrtWithEnSrt, file)
    node5 = Node(getTrSrtByName, file)
    node6 = Node(readyEnSrt, file)
    node7 = Node(getEnSrtByHash, file)
    node8 = Node(subsyncEnSrtWithAudio, file)
    node9 = Node(getEnSrtByName, file)
    node10 = Node(getTrSrtByHash, file)
    node11 = Node(getTrSrtByName, file)
    node12 = Node(readyNothing, file)
    node13 = Node(readyTrSrt, file)
    node14 = Node(subsyncTrSrtWithAudio, file)

    node1.setNexts(node2, node7)
    node2.setNexts(node3, node5)
    node3.setNexts(None, None)
    node4.setNexts(node3, None)
    node5.setNexts(node4, node6)
    node6.setNexts(None, None)
    node7.setNexts(node2, node9)
    node8.setNexts(node2, None)
    node9.setNexts(node8, node10)
    node10.setNexts(node13, node11)
    node11.setNexts(node14, node12)
    node12.setNexts(None, None)
    node13.setNexts(None, None)
    node14.setNexts(node13, None)

    node1.run()
