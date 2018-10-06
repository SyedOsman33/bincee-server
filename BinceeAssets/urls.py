from django.conf.urls import url, include

from BinceeAssets.views import add_assets, edit_assets, get_assets_list

urlpatterns = [
    url(r'^add_asset', add_assets),
    url(r'^edit_asset', edit_assets),
    url(r'^get_assets_list', get_assets_list),

]