from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListAPI.as_view()),                       # GET /api/v1/products/
    path('<int:pk>/', views.ProductDetailAPI.as_view()),            # GET /api/v1/products/1/
    # path('<int:pk>/subscribe/', views.ProductSubscribeAPI.as_view()),  # POST /api/v1/products/1/subscribe/
    path('deposit-products/subscribe/<str:fin_prdt_cd>/', views.DepositProductSubscribeAPI.as_view()),  # POST /api/v1/products/deposit-products/subscribe/1234567890/
    path('saving-products/subscribe/<str:fin_prdt_cd>/', views.SavingProductSubscribeAPI.as_view()),  # POST /api/v1/products/saving-products/subscribe/1234567890/
    path('save-deposit-products/', views.save_deposit_products),
    path('deposit-products/', views.deposit_products),
    path('deposit-product-options/<str:fin_prdt_cd>/', views.deposit_product_options),
    path('deposit-products/top-rate/', views.top_rate),
    path('deposit-products-with-options/', views.deposit_products_with_options),
    path('saving-products/', views.saving_products),
    path('saving-save/', views.save_saving_products),
    path('saving-products/top-rate/', views.Saving_product_options),
]
