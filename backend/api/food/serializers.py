from rest_framework import serializers
from .models import Shop, ImageFile

class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFile
        fields = ["id", "url"]

    def get_url(self, obj):
        # 画像ファイルが存在し、URLが利用可能であれば、絶対URLを返す
        if obj.url and hasattr(obj.url, "url"):
            request = self.context.get("request")
            if request is not None:
                return request.build_absolute_uri(obj.url.url)
            return obj.url.url # requestがない場合は相対URL
        return None

class ShopSerializer(serializers.ModelSerializer):
    image_file = ImageFileSerializer(required=False, allow_null=True)

    class Meta:
        model = Shop
        fields = '__all__'