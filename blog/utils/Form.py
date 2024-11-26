
from django import forms
from django.template.context_processors import request
from urllib import request
from blog.models import Article,User
from blog.utils.encrypt import md5
from blog.models import User

class editForm(forms.ModelForm):
    author = forms.CharField(
        label="作者",
        disabled=True,
        widget=forms.TextInput(attrs={"placeholder": "用户名"}),
    )
    boostrap_exclude_fields = []
    def __init__(self, *args, **kwargs):
        default_name = kwargs.pop('default_name', None)
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.boostrap_exclude_fields:
                continue
            if default_name:
                self.fields['author'].initial = default_name
            self.fields['desc'].widget.attrs['id'] = 'add_color'  # 你可以自定义 id 名称
            self.fields['title'].widget.attrs['id'] = 'add_color'  # 你可以自定义 id 名称
            self.fields['author'].widget.attrs['id'] = 'add_color'  # 你可以自定义 id 名称
            self.fields['cover'].widget.attrs['id'] = 'add_color'  # 你可以自定义 id 名称
            # 字段中有属性，保留原来的属性，没有属性才增加
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {"class": "form-control" }

    def clean_content(self):
        content = self.cleaned_data['content']
        if "<script>" in content or "</script>" in content:
            raise forms.ValidationError("内容中含有不安全的代码!")
        return content

    def clean_title(self):
        title = self.cleaned_data['title']
        if "<script>" in title or "</script>" in title:
            raise forms.ValidationError("内容中含有不安全的代码!")
        return title

    def clean_desc(self):
        desc = self.cleaned_data['desc']
        if "<script>" in desc or "</script>" in desc:
            raise forms.ValidationError("内容中含有不安全的代码!")
        return desc

    def clean_cover(self):
        cover = self.cleaned_data['cover']
        try:
            with request.urlopen(cover) as file:
                pass
        except Exception as e:
            raise forms.ValidationError("无效链接")
        return cover

    class Meta:
        model = Article
        fields = ['title', 'author', 'desc', 'cover', 'content', 'years', 'category', 'tag']



class RegisterForm(forms.ModelForm):
    boostrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.boostrap_exclude_fields:
                continue
            # 字段中有属性，保留原来的属性，没有属性才增加
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {"class": "form-control"}


    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "确认密码"}),
        label="确认密码",
    )
    code = forms.CharField(
        label="验证码",
        # render_value=True 密码不丢失
        widget=forms.TextInput(attrs={"placeholder": "请输入验证码"}),
    )


    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm =  md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise forms.ValidationError("两次密码输入不正确")
        else:
            return confirm

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if User.objects.filter(name=name).exists():
            raise forms.ValidationError("用户名已经存在")
        else:
            return name

    class Meta:
        model = User
        fields = ['name', 'password','email']
        widgets = {
            'password':forms.PasswordInput(render_value=True)
        }


class ResetPassword(forms.ModelForm):
    boostrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.boostrap_exclude_fields:
                continue
            # 字段中有属性，保留原来的属性，没有属性才增加
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {"class": "form-control"}

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "确认密码"}),
        label="确认密码",
    )

    code = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "输入验证码"}),
        label="验证码"
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not User.objects.filter(name=name).exists():
            raise forms.ValidationError("用户名不存在")
        else:
            return name


    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('confirm_password')
        if md5(pwd)!= self.cleaned_data.get('password'):
            raise forms.ValidationError("输入的密码不一致")
        else:
            return md5(pwd)

    class Meta:
        model = User
        fields = ['name','password', 'email']



class LoginForm(forms.ModelForm):
    boostrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.boostrap_exclude_fields:
                continue
            # 字段中有属性，保留原来的属性，没有属性才增加
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {"class": "form-control"}

    code = forms.CharField(
        label="验证码",
        # render_value=True 密码不丢失
        widget=forms.TextInput(attrs={"placeholder": "请输入验证码"}),
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


    class Meta:
        model = User
        fields = ['name','password']



