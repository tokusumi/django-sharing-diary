from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Marker


class MarkerAdmin(LeafletGeoAdmin):
    list_display = ('name', )  # 一覧に出したい項目
    list_display_links = ('name',)  # 修正リンクでクリックできる項目


admin.site.register(Marker, MarkerAdmin)
