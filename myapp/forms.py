# forms.py
from django import forms
import re

class MemberForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        error_messages={'required': '姓名是必填项'},
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        error_messages={'required': '电话是必填项'},
    )
    purchase_count = forms.IntegerField(
        min_value=1,
        required=True,
        error_messages={'required': '购买次数是必填项', 'min_value': '购买次数必须是正整数'}
    )
    remaining_count = forms.IntegerField(
        min_value=1,
        required=True,
        error_messages={'required': '剩余次数是必填项', 'min_value': '剩余次数必须是正整数'}
    )

    # 自定义姓名验证
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.match(r'^[\u4e00-\u9fa5a-zA-Z ]+$', name):
            raise forms.ValidationError('姓名不能包含特殊字符，只能包含中文、英文字母和空格')
        return name

    # 自定义电话验证
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError('电话只能包含数字')
        return phone

    # 自定义剩余次数验证
    def clean(self):
        cleaned_data = super().clean()
        purchase_count = cleaned_data.get('purchase_count')
        remaining_count = cleaned_data.get('remaining_count')

        if remaining_count and purchase_count and remaining_count > purchase_count:
            raise forms.ValidationError('剩余次数不能超过购买次数')
