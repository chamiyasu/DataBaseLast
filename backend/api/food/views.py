from django.forms import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from api.food.authentication import RefreshJWTAuthentication
from django.conf import settings
from .models import Shop, ImageFile
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ShopSerializer


class DiaryView(APIView):
    # 日記操作に関する関数で共通で使用するお店取得関数
    def get_object(self, pk):
        try:
            return Shop.objects.get(pk=pk)
        except Shop.DoesNotExist:
            raise FileNotFoundError

    """
    日記操作に関する関数
    """
    def get(self, request, id=None, format=None):
        """
        お店の一覧もしくは一意のお店を取得する
        """
        if id is None :
            queryset = Shop.objects.all()
            serializer = ShopSerializer(queryset, many=True, context={"request": request})
        else:
            shop = self.get_object(id)
            serializer = ShopSerializer(shop, context={"request": request})
        return Response(serializer.data, status.HTTP_200_OK)
    
    
    def delete(self, request, id, format=None):
        product = self.get_object(id)
        product.delete()
        return Response(status = status.HTTP_200_OK)
    
class SaveView(APIView):
    """
    お店の登録・更新時の登録処理
    """
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        image_file = request.FILES.get("image_file")  # フロント側のフォームでの画像のキーが 'image' なら
        if image_file:
            image_instance = ImageFile.objects.create(url=image_file)
            data = request.data.copy()
            data['image_file'] = image_instance.id  # ForeignKeyにIDをセット
        else:
            data = request.data

        serializer = ShopSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            print(f"Saved instance ID: {instance.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):
        shop = self.get_object(id)
        serializer = ShopSerializer(instance=shop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get_object(self, id):
    #     return get_object_or_404(Shop, pk=id)


class ShopModelViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

class LoginView(APIView):
    """ユーザーのログイン処理
    Args:
    APIView (class): rest_framework.viewsのAPIViewを受け取る
    """
    # 認証クラスの指定
    # リクエストヘッダーにtokenを差し込むといったカスタム動作をしないので素の認証クラスを使用する
    authentication_classes = [JWTAuthentication]
    # アクセス許可の指定
    permission_classes = [ ]

    def post(self, request):
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access = serializer.validated_data.get("access", None)
        refresh = serializer.validated_data.get("refresh", None)
        if access:
            response = Response(status=status.HTTP_200_OK)
            max_age = settings.COOKIE_TIME
            response.set_cookie('access', access, httponly=True, max_age=max_age)
            response.set_cookie('refresh', refresh, httponly=True, max_age=max_age)
            return response
        return Response({'errMsg': 'ユーザーの認証に失敗しました'}, status=status.HTTP_401_UNAUTHORIZED)


class RetryView(APIView):
    authentication_classes = [RefreshJWTAuthentication]
    permission_classes = []

    def post(self, request):
        request.data['refresh'] = request.META.get('HTTP_REFRESH_TOKEN')
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access = serializer.validated_data.get("access", None)
        refresh = serializer.validated_data.get("refresh", None)
        if access:
            response = Response(status=status.HTTP_200_OK)
            max_age = settings.COOKIE_TIME
            response.set_cookie('access', access, httponly=True, max_age=max_age)
            response.set_cookie('refresh', refresh, httponly=True, max_age=max_age)
            return response
        return Response({'errMsg': 'ユーザーの認証に失敗しました'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args):
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response