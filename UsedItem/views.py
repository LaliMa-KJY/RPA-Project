from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .crawling import get_all_products, get_joongna_products, get_dangn_products, get_bunjang_products
from .kakaoMSG import sendMSG as sendMsg
from . import DBController
import json, openpyxl
import pandas as pd

import requests
from django.http import JsonResponse
from django.shortcuts import redirect
from django.conf import settings


def search(request):
    print('search')

    keyword = request.GET.get('kw', '')
    print(keyword)
    if (keyword == ''):
        context = {
            'mode': 'basic'
        }
        return render(request, 'UsedItem/search.html', context=context)

    if 'keyword' in request.session:
        del request.session['keyword']
    request.session['keyword'] = keyword


    dbController = DBController.DBController()

    bunjang = get_bunjang_products(keyword)
    danggeun = get_dangn_products(keyword)
    joongna = get_joongna_products(keyword)
    items = bunjang + danggeun + joongna

    dbController.saveItems(items)

    context = {
        'mode': 'search',
        'keyword': keyword,
        'items': json.dumps(items),
        'bunjang': json.dumps(bunjang),
        'danggeun': json.dumps(danggeun),
        'joongna': json.dumps(joongna),
    }
    return render(request, 'UsedItem/search.html', context=context)



# csrf 검사 무시
@csrf_exempt
def excelSave(request):
    if request.method == 'POST':
        print('excelSave')
        dbController = DBController.DBController()
        items = dbController.getAllItems()

        dataFrame = pd.DataFrame(items)
        dataFrame.to_excel('중고매물검색결과.xlsx', index=False)

        return JsonResponse({'message':'success'})
    return JsonResponse({'error':'fail'})


def kakao_login(request):
    print('로그인')
    client_id = settings.KAKAO_CLIENT_ID
    redirect_uri = 'http://127.0.0.1:8000/oauth'
    return redirect(f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}")

def kakao_callback(request):
    print('콜백')
    code = request.GET.get('code')
    print(f'받은 코드: {code}')
    client_id = settings.KAKAO_CLIENT_ID
    redirect_uri = 'http://127.0.0.1:8000/oauth'
    token_url = 'https://kauth.kakao.com/oauth/token'
    
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'code': code,
    }
    keyword = request.session.get('keyword', '')
    response = requests.post(token_url, data=data)
    token_json = response.json()
    sendMsg(token_json, keyword)
    return render(request, 'UsedItem/kakaoSuccess.html')