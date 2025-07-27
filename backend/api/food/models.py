from django.db import models

# class Category(models.Model):
#     """
#     カテゴリー
#     """
#     name = models.CharField(max_length=100, verbose_name="カテゴリ名")
#     parent_category = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

#     class Meta:
#         db_table = "category"
#         verbose_name = "カテゴリー"

class ImageFile(models.Model):
    """
    画像ファイル
    """
    url = models.ImageField(upload_to="images/", default="shop_images/default.jpg", verbose_name="画像ファイル")

    class Meta:
        verbose_name = "画像ファイル"
        db_table = "image_file"
        
class Shop(models.Model):
    """
    お店
    """
    image_file = models.ForeignKey(
        ImageFile, on_delete=models.CASCADE, verbose_name="写真ファイルID", null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="店舗名")
    value = models.FloatField(verbose_name="店舗評価")
    description = models.TextField(verbose_name="店舗説明", null=True, blank=True)
    cite = models.TextField(verbose_name="店舗サイト", null=True, blank=True)

    class Meta:
        db_table = "shop"
        verbose_name = "店舗"
