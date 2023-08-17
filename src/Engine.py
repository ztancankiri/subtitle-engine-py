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


def initialTask(file):
    if (checkEnSrt(file)):
        checkAndFixLocalSubFileName(file, "en")
    else:
        extractEnSrtFromMkv(file)

    if (checkTrSrt(file)):
        checkAndFixLocalSubFileName(file, "tr")
    else:
        extractTrSrtFromMkv(file)

    return True


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
    if (checkAndFixLocalSubFileName(syncedSubFile, subLang)):
        return True
    else:
        if (os.path.exists(syncedSubFile)):
            os.unlink(syncedSubFile)
        return False


def subsyncEnSrtWithTrSrt(file):
    refLang = "tr"
    subLang = "en"

    refPath = findLocalSub(file, refLang)
    subPath = findLocalSub(file, subLang)

    syncedSubFile = sync(subPath, subLang, refPath, refLang)
    if (checkAndFixLocalSubFileName(syncedSubFile, subLang)):
        return True
    else:
        if (os.path.exists(syncedSubFile)):
            os.unlink(syncedSubFile)
        return False


def subsyncEnSrtWithAudio(file):
    refLang = "en"
    subLang = "en"

    refPath = file
    subPath = findLocalSub(file, subLang)

    syncedSubFile = sync(subPath, subLang, refPath, refLang)
    if (checkAndFixLocalSubFileName(syncedSubFile, subLang)):
        return True
    else:
        if (os.path.exists(syncedSubFile)):
            os.unlink(syncedSubFile)
        return False


def subsyncTrSrtWithAudio(file):
    refLang = "en"
    subLang = "tr"

    refPath = file
    subPath = findLocalSub(file, subLang)

    syncedSubFile = sync(subPath, subLang, refPath, refLang)
    if (checkAndFixLocalSubFileName(syncedSubFile, subLang)):
        return True
    else:
        if (os.path.exists(syncedSubFile)):
            os.unlink(syncedSubFile)
        return False


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
    node1 = Node(initialTask, file)
    node2 = Node(checkEnSrt, file)
    node3 = Node(checkTrSrt, file)
    node4 = Node(readyTrSrtAndEnSrt, file)
    node5 = Node(getTrSrtByHash, file)
    node6 = Node(subsyncTrSrtWithEnSrt, file)
    node7 = Node(getTrSrtByName, file)
    node8 = Node(readyEnSrt, file)
    node9 = Node(getEnSrtByHash, file)
    node10 = Node(checkTrSrt, file)
    node11 = Node(getTrSrtByHash, file)
    node12 = Node(getTrSrtByName, file)
    node13 = Node(getEnSrtByName, file)
    node14 = Node(subsyncTrSrtWithEnSrt, file)
    node15 = Node(checkTrSrt, file)
    node16 = Node(checkTrSrt, file)
    node17 = Node(subsyncEnSrtWithTrSrt, file)
    node18 = Node(readyTrSrt, file)
    node19 = Node(getTrSrtByHash, file)
    node20 = Node(getTrSrtByHash, file)
    node21 = Node(subsyncTrSrtWithAudio, file)
    node22 = Node(getTrSrtByName, file)
    node23 = Node(subsyncEnSrtWithAudio, file)
    node24 = Node(readyNothing, file)
    node25 = Node(getTrSrtByName, file)
    node26 = Node(subsyncTrSrtWithEnSrt, file)
    node27 = Node(getTrSrtByName, file)
    node28 = Node(subsyncTrSrtWithAudio, file)

    node1.setNexts(node2, None)
    node2.setNexts(node3, node9)
    node3.setNexts(node4, node5)
    node4.setNexts(None, None)
    node5.setNexts(node4, node7)
    node6.setNexts(node4, None)
    node7.setNexts(node6, node8)
    node8.setNexts(None, None)
    node9.setNexts(node10, node13)
    node10.setNexts(node4, node11)
    node11.setNexts(node4, node12)
    node12.setNexts(node14, node8)
    node13.setNexts(node16, node15)
    node14.setNexts(node4, None)
    node15.setNexts(node18, node19)
    node16.setNexts(node17, node20)
    node17.setNexts(node4, node18)
    node18.setNexts(None, None)
    node19.setNexts(node18, node22)
    node20.setNexts(node17, node23)
    node21.setNexts(node18, node24)
    node22.setNexts(node21, node24)
    node23.setNexts(node25, None)
    node24.setNexts(None, None)
    node25.setNexts(node26, node8)
    node26.setNexts(node4, node8)
    node27.setNexts(node28, node24)
    node28.setNexts(node18, node24)

    node1.run()
