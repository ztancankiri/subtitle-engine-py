import os
import guessit
import requests
import xml.etree.ElementTree as ET
from Utils import convertToUTF8BOM, normalizeText, xml_to_dict
from zipfile import ZipFile
from io import BytesIO


class OpenSubtitles:
    def __init__(self):
        self.chunkSize = 64 * 1024
        self.baseUrl = "http://api.opensubtitles.org/xml-rpc"
        self.userAgent = "VLSub"
        self.contentType = "text/xml"

    def hashChunk(self, file, position):
        cursor = position
        hash_value = 0

        for _ in range(8192):
            buffer = bytearray(8)
            file.seek(cursor)
            buffer = file.read(8)
            cursor += 8

            hash_value += int.from_bytes(buffer,
                                         byteorder='little', signed=True)
            hash_value &= 0xFFFFFFFFFFFFFFFF

        return hash_value

    def hashFile(self, file):
        size = os.path.getsize(file)

        if size < self.chunkSize * 2:
            return "SizeError"

        hash_value = size

        with open(file, "rb") as file:
            hash_value += self.hashChunk(file, 0)
            hash_value &= 0xFFFFFFFFFFFFFFFF

            hash_value += self.hashChunk(file, max(0, size - self.chunkSize))
            hash_value &= 0xFFFFFFFFFFFFFFFF

        return format(hash_value, '016x')

    def post(self, body):
        try:
            headers = {
                "User-Agent": self.userAgent,
                "Content-Type": self.contentType
            }

            response = requests.post(self.baseUrl, data=body, headers=headers)
            response.raise_for_status()

            return ET.fromstring(response.text)

        except requests.exceptions.RequestException as error:
            print(error)

    def parse(self, inputData):
        data = xml_to_dict(inputData)
        data = data['params']['param']['value']['struct']['member'][1]['value']['array']['data']

        if (data == {}):
            return []

        results = []
        dataList = data['value']

        if (len(dataList) == 1):
            dataList = [data['value']]

        for result in dataList:
            members = result['struct']['member']

            item = {}
            for member in members:
                name = member['name']
                value = None

                if "string" in member['value']:
                    value = member['value']['string']

                if "int" in member['value']:
                    value = int(member['value']['int'])

                if "double" in member['value']:
                    value = float(member['value']['double'])

                item[name] = value
            results.append(item)

        return results

    def login(self):
        body = """<?xml version='1.0'?>
        <methodCall>
         <methodName>LogIn</methodName>
         <params>
          <param><value></value></param>
          <param><value></value></param>
          <param><value><string>eng</string></value></param>
          <param><value><string>VLSub 0.11.1</string></value></param>
         </params>
        </methodCall>"""

        response = self.post(body)
        token = response.find(
            'params/param/value/struct/member/value/string').text

        return token

    def searchHash(self, token, language, file):
        hashValue = self.hashFile(file)
        size = os.path.getsize(file)

        body = f"""<?xml version='1.0'?>
            <methodCall>
             <methodName>SearchSubtitles</methodName>
             <params>
              <param><value><string>{token}</string></value></param>
              <param>
               <value>
                <array>
                 <data>
                  <value>
                   <struct>
                    <member><name>sublanguageid</name><value><string>{language}</string></value></member>
                    <member><name>moviehash</name><value><string>{hashValue}</string></value></member>
                    <member><name>moviebytesize</name><value><double>{size}</double></value></member>
                   </struct>
                  </value>
                 </data>
                </array>
               </value>
              </param>
             </params>
            </methodCall>"""

        response = self.post(body)
        return self.parse(response)

    def searchName(self, token, language, file):
        name = os.path.basename(file)
        info = dict(guessit.guessit(name))

        query = ""
        season = ""
        episode = ""

        if (info["type"] == "movie"):
            query = info["title"]

            if ("year" in info):
                query += " " + str(info["year"])

            if ("screen_size" in info and len(info["screen_size"]) > 0):
                query += " " + str(info["screen_size"])

            if ("source" in info and len(info["source"]) > 0):
                query += " " + str(info["source"])
        elif (info["type"] == "episode"):
            query = str(info["title"])

            if ("screen_size" in info and len(info["screen_size"]) > 0):
                query += " " + str(info["screen_size"])

            if ("season" in info):
                season = info["season"]

            if ("episode") in info:
                episode = info["episode"]

        query = normalizeText([query])

        body = f"""<?xml version='1.0'?>
            <methodCall>
             <methodName>SearchSubtitles</methodName>
             <params>
              <param><value><string>{token}</string></value></param>
              <param>
               <value>
                <array>
                 <data>
                  <value>
                   <struct>
                    <member><name>sublanguageid</name><value><string>{language}</string></value></member>
                    <member><name>query</name><value><string>{query}</string></value></member>
                    <member><name>season</name><value><string>{season}</string></value></member>
                    <member><name>episode</name><value><string>{episode}</string></value></member>
                   </struct>
                  </value>
                 </data>
                </array>
               </value>
              </param>
             </params>
            </methodCall>"""

        response = self.post(body)
        return self.parse(response)

    def download(self, url):
        try:
            headers = {
                "User-Agent": self.userAgent,
                "Content-Type": self.contentType
            }

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            buffer = BytesIO(response.content)

            with ZipFile(buffer) as zip_archive:
                return [
                    {
                        "name": entry.filename,
                        "data": convertToUTF8BOM(zip_archive.read(entry)),
                    }
                    for entry in zip_archive.infolist()
                    if (not entry.is_dir() and (entry.filename.endswith(".srt")))
                ]
        except requests.exceptions.RequestException as error:
            print(error)
