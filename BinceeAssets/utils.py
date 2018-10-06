from BinceeAssets.models import BinceeEntities
from BinceeAssets.serializers import BinceeAssetsSerializer


def get_all_assets_of_type(type_id, context):
    if type_id:
        assets_q_set = BinceeEntities.objects.filter(type_id=type_id)

        serializer = BinceeAssetsSerializer(assets_q_set, many=True, context=context)
        data = serializer.data
        return data
    else:
        return []

