import requests
from bs4 import BeautifulSoup
import io
import rarfile
import json

def get_file(subtitle_url):
    response = requests.get(subtitle_url)
    
    soup = BeautifulSoup(response.text, "html.parser")
    token = soup.find('input', {'name': '_token'})["value"]

    download_btn = soup.find("a", class_="download_btn_enable")
    subtitle_id = download_btn["rel-id"]
    uniquekey = download_btn["rel-tag"]

    cookies = response.cookies.get_dict()
    payload = {
        '_token': token,
        '_method': 'POST',
        'subtitle_id': subtitle_id,
        'uniquekey': uniquekey,
        'filepath': ''
    }

    response = requests.post("https://www.planetdp.org/subtitle/download", data=payload, cookies=cookies, stream=True)

    rar_buffer = io.BytesIO(response.content)
    with rarfile.RarFile(rar_buffer) as rf:
        for file_info in rf.infolist():
            rf.extract(file_info, ".")

def get_subtitles(imdb_id):
    try:
        query_url = f"https://www.planetdp.org/movie/search/?title={imdb_id}"
        query_response = requests.get(query_url)
        query_response.raise_for_status()

        soup = BeautifulSoup(query_response.text, "html.parser")
        table = soup.find("table", {"id": "subtable"})
        tbody_elements = [tbody for tbody in table.find_all("tbody") if tbody.text.strip()]

        result = []

        for tbody in tbody_elements:
            tr_elements = tbody.find_all("tr", class_=["row1", "row2"])
            
            for j in range(0, len(tr_elements), 2):
                tr = tr_elements[j]
                block = tr.find("td", class_="t-content-one")
                subtitle = {}
                subtitle["title"] = block.find("a").text.strip()
                
                temp = block.find('span', attrs={'itemprop': lambda x: x != 'subtitleLanguage'})

                if (temp is not None):
                    temp = temp.text.strip()
                    if ("-" in temp):
                        temp = temp.split("-")
                        subtitle["season"] = temp[0].split(":")[1]
                        subtitle["episode"] = temp[1].split(":")[1]
                
                subtitle["lang"] = block.find("span", attrs={"itemprop": "subtitleLanguage"}).text.strip()
                subtitle["fps"] = tr.find("td", class_=["t-content3"]).text.strip()
                subtitle["files"] = tr.find("td", class_=["t-content4"]).text.strip()
                subtitle["format"] = tr.find("td", class_=["t-content6"]).text.strip()
                subtitle["translator"] = tr.find("td", class_=["t-content5"]).text.strip()
                subtitle["download"] = "https://planetdp.org" + tr.find("a", class_=["download-btn"])["href"]

                tds = tr_elements[j + 1].find("td", class_=lambda x: x != "tdcen")
                for td in tds:
                    txt = td.text.strip()
                    if ("Sürüm:" in txt):
                        subtitle["release"] = txt.split("Sürüm:")[1].strip()
                    
                    if ("Not:" in txt):
                        subtitle["notes"] = txt.split("Not:")[1].strip()

                if (temp is None):
                    result.append(subtitle)
                else:
                    isAdded = False
                    for k in range(len(result)):
                        if (result[k]["season"] == subtitle["season"]):
                            result[k]["subtitles"].append(subtitle)
                            isAdded = True
                    
                    if (not isAdded):
                        result.append({
                            "season": subtitle["season"],
                            "subtitles": [ subtitle ]
                        })

        return result
    except Exception as e:
        print(e)
    
    return []

# print(json.dumps(get_subtitles("tt0411008"), indent=4))

url = "https://planetdp.org/subtitle/lost-sub6964"

get_file(url)