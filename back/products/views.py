from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Product,DepositProducts, DepositOptions, SavingProducts, SavingOptions
from accounts.models import UserSubscription, SavingSubscription
from .serializers import (
    DepositProductsSerializer, DepositOptionsSerializer,
    SavingProductsSerializer, SavingOptionsSerializer,ProductSerializer
)
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from django.shortcuts import get_list_or_404, get_object_or_404



# 전체 조회
class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# 상세 조회
class ProductDetailAPI(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# # 가입하기 (로그인 필요)
# class ProductSubscribeAPI(generics.GenericAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = Product.objects.all()

#     def post(self, request, pk):
#         product = self.get_object()
#         request.user.subscribed.add(product)  # User.subscribed M2M 필드
#         return Response({'detail': '가입 완료'}, status=status.HTTP_200_OK)

class DepositProductSubscribeAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DepositProducts.objects.all()
    lookup_field = 'fin_prdt_cd'
    lookup_url_kwarg = 'fin_prdt_cd'

    def post(self, request, fin_prdt_cd):
        product = self.get_object()
        term_months = request.data.get('term_months')
        if not term_months:
            return Response({'error': '가입 기간을 선택해주세요'},
                            status=status.HTTP_400_BAD_REQUEST)

        UserSubscription.objects.create(
            user=request.user,
            product=product,
            term_months=term_months
        )
        return Response({'detail': '예금 상품 가입이 완료되었습니다'})

    def delete(self, request, fin_prdt_cd):
        product = self.get_object()
        # 해당 구독 레코드만 삭제
        UserSubscription.objects.filter(
            user=request.user, product=product
        ).delete()
        return Response({'detail': '예금 가입 취소 완료'})


class SavingProductSubscribeAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SavingProducts.objects.all()
    lookup_field = 'fin_prdt_cd'
    lookup_url_kwarg = 'fin_prdt_cd'

    def post(self, request, fin_prdt_cd):
        product = self.get_object()
        term_months = request.data.get('term_months')
        if not term_months:
            return Response({'error': '가입 기간을 선택해주세요'},
                            status=status.HTTP_400_BAD_REQUEST)

        SavingSubscription.objects.create(
            user=request.user,
            product=product,
            term_months=term_months
        )
        return Response({'detail': '적금 상품 가입이 완료되었습니다'})

    def delete(self, request, fin_prdt_cd):
        product = self.get_object()
        SavingSubscription.objects.filter(
            user=request.user, product=product
        ).delete()
        return Response({'detail': '적금 가입 취소 완료'})
@api_view(['GET'])
def save_deposit_products(request):

    # if DepositOptions.objects.exists():
    #     return Response({'message':'DB에 이미 데이터가 있습니다.'},status=status.HTTP_400_BAD_REQUEST)

    url = (
        f"https://finlife.fss.or.kr/finlifeapi/"
        f"depositProductsSearch.json?auth={settings.FINLIFE_API_KEY}"
        f"&topFinGrpNo=020000&pageNo=1"
    )

    data = requests.get(url).json().get('result', {})
    baseList = data.get('baseList', [])
    optionList = data.get('optionList', [])

    for product in baseList:
        product_serializer = DepositProductsSerializer(data={
            'fin_prdt_cd': product.get('fin_prdt_cd'),
            'kor_co_nm': product.get('kor_co_nm', ''),
            'fin_prdt_nm': product.get('fin_prdt_nm', ''),
            'etc_note': product.get('etc_note', ''),
            'join_deny': int(product.get('join_deny') or 1),
            'join_member': product.get('join_member', ''),
            'join_way': product.get('join_way', ''),
            'spcl_cnd': product.get('spcl_cnd', ''),
        })
        if product_serializer.is_valid(raise_exception=True):
            prod=product_serializer.save()
    
    for option in optionList:
        prod=DepositProducts.objects.get(fin_prdt_cd=option.get('fin_prdt_cd'))
        option_serializer = DepositOptionsSerializer(data={ 
            'fin_prdt_cd': option.get('fin_prdt_cd', ''),
            'intr_rate_type_nm': option.get('intr_rate_type_nm', ''),
            'intr_rate': float(option.get('intr_rate') or -1),
            'intr_rate2': float(option.get('intr_rate2') or -1),
            'save_trm': int(option.get('save_trm') or 0),
        })
        if option_serializer.is_valid(raise_exception=True):
            option_serializer.save(product=prod)    
            
    return Response(
        {'message':'OK'},
        status=status.HTTP_201_CREATED
    )


@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'GET':
        products = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(products, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        fin_prdt_cd = request.data.get('fin_prdt_cd')
    
        if DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            return Response(
                {'error': f'상품 코드 {fin_prdt_cd}는 이미 존재합니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = DepositProductsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'error': f'유효하지않은 정보. 저장되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    options = get_list_or_404(DepositOptions, fin_prdt_cd=fin_prdt_cd)
    serializer = DepositOptionsSerializer(options, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def top_rate(request):
    best_option = DepositOptions.objects.order_by('-intr_rate2').first()
    if not best_option:
        return Response({"error": "데이터가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
    product = best_option.product
    options = DepositOptions.objects.filter(product=product)
    product_serializer = DepositProductsSerializer(product)
    option_serializer = DepositOptionsSerializer(options, many=True)
    return Response({
        "product": product_serializer.data,
        "options": option_serializer.data
    })

@api_view(['GET'])
def deposit_products_with_options(request):
    qs = DepositProducts.objects.prefetch_related('options').all()
    serializer = DepositProductsSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def save_saving_products(request):

    # if DepositOptions.objects.exists():
    #     return Response({'message':'DB에 이미 데이터가 있습니다.'},status=status.HTTP_400_BAD_REQUEST)

    url = (
        f"https://finlife.fss.or.kr/finlifeapi/"
        f"savingProductsSearch.json?auth={settings.FINLIFE_API_KEY}"
        f"&topFinGrpNo=020000&pageNo=1"
    )

    data = requests.get(url).json().get("result", {})
    baseList = data.get("baseList", [])
    optionList = data.get("optionList", [])

    for product in baseList:
        product_serializer = SavingProductsSerializer(
            data={
                "fin_prdt_cd": product.get("fin_prdt_cd"),
                "kor_co_nm": product.get("kor_co_nm", ""),
                "fin_prdt_nm": product.get("fin_prdt_nm", ""),
                "etc_note": product.get("etc_note", ""),
                "join_deny": int(product.get("join_deny") or 1),
                "join_member": product.get("join_member", ""),
                "join_way": product.get("join_way", ""),
                "spcl_cnd": product.get("spcl_cnd", ""),
            }
        )
        if product_serializer.is_valid(raise_exception=True):
            prod = product_serializer.save()

    for option in optionList:
        prod = SavingProducts.objects.get(fin_prdt_cd=option.get("fin_prdt_cd"))
        option_serializer = SavingOptionsSerializer(
            data={
                "fin_prdt_cd": option.get("fin_prdt_cd", ""),
                "intr_rate_type_nm": option.get("intr_rate_type_nm", ""),
                "intr_rate": float(option.get("intr_rate") or -1),
                "intr_rate2": float(option.get("intr_rate2") or -1),
                "save_trm": int(option.get("save_trm") or 0),
            }
        )
        if option_serializer.is_valid(raise_exception=True):
            option_serializer.save(product=prod)

    return Response({"message": "OK"}, status=status.HTTP_201_CREATED)


@api_view(["GET", "POST"])
def saving_products(request):
    if request.method == "GET":
        products = SavingProducts.objects.all()
        serializer = SavingProductsSerializer(products, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        fin_prdt_cd = request.data.get("fin_prdt_cd")

        if SavingProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            return Response(
                {"error": f"상품 코드 {fin_prdt_cd}는 이미 존재합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SavingProductsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"error": f"유효하지않은 정보. 저장되지 않았습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
def Saving_product_options(request, fin_prdt_cd):
    options = get_list_or_404(SavingOptions, fin_prdt_cd=fin_prdt_cd)
    serializer = SavingOptionsSerializer(options, many=True)
    return Response(serializer.data)
