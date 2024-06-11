from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .crawling import get_all_products, get_joongna_products, get_dangn_products, get_bunjang_products
from .kakaoMSG import sendMSG as sendMsg
from . import DBController
import json

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

    # 검색 수행할 때마다 db 비워주기
    dbController = DBController.DBController()

    bunjang = get_bunjang_products(keyword)
    # @TODO 당근, 중고나라 넣기
    # danggeun = get_dangn_products(keyword)
    # joongna = get_joongna_products(keyword)
    # items = {'bunjang': bunjang, 'danggeun':danggeun, 'joongna':joongna}
    # items = bunjang + danggeun + joongna
    items = bunjang
    dbController.saveItems(items)

    # @TODO 당근, 중고나라 넣기
    context = {
        'mode': 'search',
        'keyword': keyword,
        'items': json.dumps(items),
        'bunjang': json.dumps(bunjang),
        # 'danggeun': json.dumps(danggeun),
        # 'joongna': json.dumps(joongna),
    }
    return render(request, 'UsedItem/search.html', context=context)



# csrf 검사 무시
@csrf_exempt
def excelSave(request):
    if request.method == 'POST':
        print('excelSave')
        return JsonResponse({'message':'success'})
    return JsonResponse({'error':'fail'})

def myTest(request):
    print('myTest')
    keyword = '아이폰'
    items = get_all_products(keyword)
    if 'products' in request.session:   # 기존 세션에 저장된 데이터 비우기
        del request.session['products']
    request.session['products'] = items
    saved_products = request.session.get('products')
    if saved_products:
        print("세션에 데이터가 저장되었습니다.")
        print(saved_products)  # 로그에 출력
    else:
        print("세션에 데이터가 저장되지 않았습니다.")

    context = {
        'items': json.dumps(items)
    }
    return render(request, 'UsedItem/myTest.html', context=context)





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