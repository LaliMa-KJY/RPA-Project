from django.shortcuts import render
from .crawling import get_all_products, get_joongna_products, get_dangn_products, get_bunjang_products

import json



def search(request):
    print('search')

    keyword = request.GET.get('kw', '')
    print(keyword)
    if (keyword == ''):
        context = {
            'mode': 'basic'
        }
        return render(request, 'UsedItem/search.html', context=context)
    
    bunjang = get_bunjang_products(keyword)
    # danggeun = get_dangn_products(keyword)
    # joongna = get_joongna_products(keyword)
    # items = {'bunjang': bunjang, 'danggeun':danggeun, 'joongna':joongna}
    items = {'bunjang': bunjang}


    context = {
        'mode': 'search',
        'items': json.dumps(items),
        'bunjang': json.dumps(bunjang),
        # 'danggeun': json.dumps(danggeun),
        # 'joongna': json.dumps(joongna),
    }
    return render(request, 'UsedItem/search.html', context=context)




def kakaoMSG(request):
    print('kakaoMSG')
    return render(request, 'UsedItem/myTest.html')

def excelSave(request):
    print('excelSave')
    return render(request, 'UsedItem/myTest.html')

def myTest(request):
    print('myTest')
    keyword = '아이폰'
    items = get_all_products(keyword)
    if 'products' in request.session:   # 기존 세션에 저장된 데이터 비우기
        del request.session['products']
    request.session['products'] = items
    # request.session['products'] = json.dumps(items)
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