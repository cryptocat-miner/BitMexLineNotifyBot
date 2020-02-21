import requests
import io

lineNotifyToken = "LINE NotifyのAPIキーを入れてください"
lineNotifyApi = "https://notify-api.line.me/api/notify"
headers = {"Authorization": "Bearer " + lineNotifyToken}


def PostMessage(message: str):
    payload = {"message": "\r\n" + message}
    try:
        requests.post(url=lineNotifyApi, data=payload, headers=headers)
    except Exception as error:
        print(error)


def PostImageFile(message: str, imageFile: io.BytesIO):
    payload = {"message": "\r\n" + message}
    files = {"imageFile": imageFile}
    try:
        requests.post(url=lineNotifyApi, data=payload, headers=headers, files=files)
    except Exception as error:
        print(error)
