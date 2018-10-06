__author__ = 'SyedUsman'
__version__ = '0.1'

import traceback

from django.contrib.auth import get_user_model
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer



User = get_user_model()



class UserLoginSerializer(ModelSerializer):
    avatar_method = SerializerMethodField('img_url', required=False)

    def img_url(self, obj):
        if self.context['request'].method == 'POST' or self.context['request'].method == 'PATCH':
            req = self.context['request']
            obj.avatar = req.data.get('avatar')
            obj.save()
        elif self.context['request'].method == 'GET':
            try:
                photo_url = obj.avatar.url
                return self.context['request'].build_absolute_uri(photo_url)
            except:
                traceback.print_exc()
                return None

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'avatar_method',
        ]


class UserSerializer(ModelSerializer):
    # avatar = ImageField(allow_empty_file=True, allow_null=True, required=False)
    avatar_method = SerializerMethodField('img_url', required=False)
    full_name = SerializerMethodField('full_name_method', allow_null=True, required=False, read_only=True)
    gender_label = SerializerMethodField('gender_method', required=False, allow_null=True)
    status_label = SerializerMethodField('status_method', required=False, allow_null=True)
    # customer_name = SerializerMethodField('customer_name_method', required=False, allow_null=True)
    role_name = SerializerMethodField('role_method', required=False, allow_null=True)
    last_user_login = SerializerMethodField('last_user_login_method', required=False, allow_null=True)
    date_joined_date = SerializerMethodField('date_joined_method', required=False, allow_null=True)

    def last_user_login_method(self, obj):
        if obj.last_login:
            return obj.last_login
        else:
            return None

    def role_method(self, obj):
        if obj.role:
            role_name = obj.role.name
            return role_name
        else:
            return None

    def status_method(self, obj):
        if obj.status:
            return obj.status.label
        else:
            return None

    def customer_name_method(self, obj):
        if obj.customer:
            return obj.customer.name
        else:
            return None

    def date_joined_method(self, obj):
        if obj.created_datetime:
            return str(obj.created_datetime.date())
        else:
            return None

    def gender_method(self, obj):
        if obj.gender:
            return obj.gender.label
        else:
            return None

    def full_name_method(self, obj):
        if [obj.first_name, obj.last_name] is not None:
            full_name = obj.first_name + " " + obj.last_name
            return full_name
        else:
            return None

    def img_url(self, obj):
        if self.context['request'].method == 'POST' or self.context['request'].method == 'PATCH':
            req = self.context['request']
            obj.avatar = req.data.get('avatar')
            obj.save()
        elif self.context['request'].method == 'GET':
            try:
                photo_url = obj.avatar.url
                return self.context['request'].build_absolute_uri(photo_url)
            except:
                traceback.print_exc()
                return None

    # password = make_password()
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',

            'first_name',
            'last_name',
            'full_name',

            # 'customer',
            # 'customer_name',

            'gender',
            'gender_label',
            'status',
            'status_label',

            'modified_by',
            'role',
            'role_name',

            'contact_number',
            'date_joined_date',

            'avatar',
            'avatar_method',

            'last_user_login',

        ]

