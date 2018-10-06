import traceback

from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

import BinceeAssets


class BinceeAssetsSerializer(ModelSerializer):
    photo_method = SerializerMethodField('img_url', required=False)

    def img_url(self, obj):
        if self.context['request'].method == 'POST' or self.context['request'].method == 'PATCH':
            req = self.context['request']
            obj.avatar = req.data.get('avatar')
            obj.save()
        elif self.context['request'].method == 'GET':
            try:
                photo_url = obj.photo.url
                return self.context['request'].build_absolute_uri(photo_url)
            except:
                traceback.print_exc()
                return None

    class Meta:
        model = BinceeAssets

        fields = [
        'name',   # FULL NAME
        'type',
        'description',
        'dob',
        'photo_method',
        ]
