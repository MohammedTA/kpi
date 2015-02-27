from django.forms import widgets
from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer
from rest_framework.reverse import reverse_lazy
from kpi.models import SurveyAsset
from kpi.models import Collection

from django.contrib.auth.models import User


class Paginated(PaginationSerializer):
    root = serializers.SerializerMethodField('get_parent_url', read_only=True)

    def get_parent_url(self, obj):
        request = self.context.get('request', None)
        return reverse_lazy('api-root', request=request)


class SurveyAssetSerializer(serializers.HyperlinkedModelSerializer):
    ownerName = serializers.ReadOnlyField(source='owner.username')
    owner = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    tableView = serializers.HyperlinkedIdentityField(view_name='surveyasset-tableview')
    parent = serializers.SerializerMethodField('get_parent_url', read_only=True)
    assetType = serializers.ReadOnlyField(read_only=True, source='asset_type')
    collectionName = serializers.ReadOnlyField(read_only=True, source='collection.name')
    collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all(), allow_null=True, required=False)
    collectionLink = serializers.HyperlinkedRelatedField(source='collection', view_name='collection-detail', read_only=True)

    class Meta:
        model = SurveyAsset
        fields = ('url', 'parent', 'tableView', 'owner', 'ownerName', 'collection',
                    'settings', 'assetType', 'collectionLink',
                    'collectionName', 'uid', 'title', 'content')

    def get_parent_url(self, obj):
        request = self.context.get('request', None)
        return reverse_lazy('surveyasset-list', request=request)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    survey_assets = serializers.HyperlinkedRelatedField(many=True,
                 view_name='surveyasset-detail', read_only=True)
    class Meta:
        model = User
        fields = ('url', 'username', 'survey_assets', 'collections')

class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)

    class Meta:
        model = Collection
        fields = ('name', 'url', 'survey_assets', 'collections', 'uid', 'owner')