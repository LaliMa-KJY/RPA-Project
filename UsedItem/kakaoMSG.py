from django.conf import settings
import json, requests, response

def sendMSG(token):
    print('sendMSG')
    keyword = '아이폰'
    url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
    headers = {'Authorization': 'Bearer ' + token['access_token']}

    template_data = {
        "object_type": "list",
        "header_title": "중고매물 플랫폼 리스트",
        "header_link": {
            "web_url" : "https://m.bunjang.co.kr",
            "mobile_web_url" : "https://m.bunjang.co.kr"
        },
        "contents" : [
            {
                "title": "번개장터 - "+keyword,
                "image_url": "https://about.daangn.com/static/63d3abb868d7a650b4c0383be7891252/e9ec68d0-e49d-4071-bf92-78ed3355003f_profile_daangn.png",
                "image_width": 35,
                "image_height": 50,
                "description": "번개장터3 - "+keyword,
                "link": {
                    "web_url": "https://m.bunjang.co.kr/search/products?order=score&page=1&q="+keyword,
                    "mobile_url": "https://m.bunjang.co.kr/search/products?order=score&page=1&q="+keyword
                }
            },
            {
                "title": "2번개장터 - "+keyword,
                "image_url": "https://about.daangn.com/static/63d3abb868d7a650b4c0383be7891252/e9ec68d0-e49d-4071-bf92-78ed3355003f_profile_daangn.png",
                "image_width": 35,
                "image_height": 50,
                "description": "번개장터3 - "+keyword,
                "link": {
                    "web_url": "https://m.bunjang.co.kr/search/products?order=score&page=1&q="+keyword,
                    "mobile_url": "https://m.bunjang.co.kr/search/products?order=score&page=1&q="+keyword
                }
            },
            {
                "title": "3번개장터 - "+keyword,
                "image_url": "https://about.daangn.com/static/63d3abb868d7a650b4c0383be7891252/e9ec68d0-e49d-4071-bf92-78ed3355003f_profile_daangn.png",
                "image_width": 35,
                "image_height": 50,
                "description": "번개장터3 - "+keyword,
                "link": {
                    "web_url": "https://m.bunjang.co.kr/search/products?order=score&page=1&q="+keyword,
                    "mobile_url": "https://m.bunjang.co.kr/search/products?order=score&page=1&q="+keyword
                }
            },
        ],
        "buttons": [
            {
                "title": "번장",
                "link": {
                    "web_url" : "https://m.bunjang.co.kr",
                    "mobile_web_url" : "https://m.bunjang.co.kr"
                }
            },
            {
                "title": "번장432",
                "link": {
                    "web_url" : "https://m.bunjang.co.kr",
                    "mobile_web_url" : "https://m.bunjang.co.kr"
                }
            },
        ]
    }

    data = {"template_object": json.dumps(template_data)}

    res = requests.post(url, headers=headers, data=data)

    if res.status_code != 200 :
        print("fail")
        print(res.json())
    else :
        print("success")