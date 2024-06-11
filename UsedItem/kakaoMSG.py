from django.conf import settings
import json, requests, response

def sendMSG(token, keyword):
    print('sendMSG')
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
                "title": "당근마켓 - "+keyword,
                "image_url": "https://about.daangn.com/static/63d3abb868d7a650b4c0383be7891252/e9ec68d0-e49d-4071-bf92-78ed3355003f_profile_daangn.png",
                "image_width": 35,
                "image_height": 50,
                "description": "당근마켓 검색 - "+keyword,
                "link": {
                    "web_url": "https://www.daangn.com/search/"+keyword,
                    "mobile_url": "https://www.daangn.com/search/"+keyword
                }
            },
            {
                "title": "번개장터 - "+keyword,
                "image_url": "https://i.namu.wiki/i/WtIn9sENtQDGxSt9Ixci74bkkW_KEXX_7HmNuwaK2bPe8gKqpubnaimFbz8uDllNkBkYhtGJwqdhRiRy_Dp15wyiRezTmiQLeEvOS9c8k-OIdUcNCvRb6yMZRSF3RZt0UiBCKK_q8f8in_HS2tgd-g.svg",
                "image_width": 35,
                "image_height": 50,
                "description": "번개장터 검색 - "+keyword,
                "link": {
                    "web_url": "https://m.bunjang.co.kr/search/products?order=score&page=1&q="+keyword,
                    "mobile_url": "https://m.bunjang.co.kr/search/products?order=score&page=1&q="+keyword
                }
            },
            {
                "title": "중고나라 - "+keyword,
                "image_url": "https://i.namu.wiki/i/iTiYG8NVHKbDXzLqNuHsJrUNJMDaDR-KxhRB-MyBKzxAyg1-n_W2yGlJn_5syIxVOwmiOLWtX0_NnFMqx-4NP2gF-mRJixp1OxZ19gwmZBv3h67B_jvCdskvf40FwCi5UUuD9PTlKNOKVP0E37J9KQ.svg",
                "image_width": 80,
                "image_height": 50,
                "description": "중고나라 검색 - "+keyword,
                "link": {
                    "web_url": "https://web.joongna.com/search/"+keyword,
                    "mobile_url": "https://web.joongna.com/search/"+keyword
                }
            },
        ],
        "buttons": [
            {
                "title": "당근",
                "link": {
                    "web_url" : "https://www.daangn.com",
                    "mobile_web_url" : "https://www.daangn.com"
                }
            },
            {
                "title": "번개장터",
                "link": {
                    "web_url" : "https://m.bunjang.co.kr",
                    "mobile_web_url" : "https://m.bunjang.co.kr"
                }
            },
            {
                "title": "중고나라",
                "link": {
                    "web_url" : "https://web.joongna.com",
                    "mobile_web_url" : "https://web.joongna.com"
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