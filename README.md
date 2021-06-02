# Django CRUD app on Docker

Django + Nginx + Gunicorn + Dockerのリポジトリです。以下の書籍を踏襲し、Django 3.2に対応。またDockerでフレキシブルな構成にしています。

- 『現場で使えるDjangoの教科書《基礎編》』
- 『現場で使えるDjangoの教科書《実践編》』

### 「現場で使えるDjangoの教科書《基礎編》」のベストプラクティス一覧

1. 分かりやすいプロジェクト構成
2. アプリケーションごとにurls.pyを配置する
3. Userモデルを拡張する
4. 発行されるクエリを確認する
5. select_related / prefetch_relatedでクエリ本数を減らす
6. ベーステンプレートを用意する
7. こんなときはModelFormを継承しよう
8. メッセージフレームワークを使う


#### 1. 分かりやすいプロジェクト構成

・問題点
- ベースディレクトリと設定ディレクトリ名が同じでややこしい
- テンプレートと静的ファイルがアプリケーションごとにバラバラに配置されてしまう

・ベストプラクティス
- startprojectで生成されるディレクトリ名を変更する。「config」「default」「root」など。
- 後述の「静的ファイル関連の設定」で対応

```bash[bash]
mkdir mysite && cd mysite
django-admin startproject config .

tree
mysite
 |-- manage.py
 `== config
    |== __init__.py
```


#### 2. アプリケーションごとにurls.pyを配置する

startproject実行時に生成されるurls.pyのみにURLパターンの設定を追加していくと、設定がどんどん肥大化して管理が大変になる。urls.pyを分割し、アプリケーションディレクトリごとに1つずつurls.pyを配置する。

```python[config/urls.py]
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
  path('admin/', admin.site.urls),
  path('item/', include('item.urls)),
]
```

include関数を使ってアプリケーションごとのurls.pyを読み込む。「/item/」で始まるURLパターンのすべてを「item」アプリケーションのitem/urls.pyに任せる。各アプリケーションのurls.pyでは、アプリケーション内部のURLパターンの設定のみに集中できる。

```python[item/urls.py]
from django.urls import path

from . import views

app_name = 'item'
urlpatterns = [
  path('', views.itemList, name='item.list'),
  path('/<int:pk>', views.itemShow, name='item.show'),
]
```

・注意点
- startappコマンドでは、アプリケーションディレクトリ内にurls.pyは生成されないので、自分で作成する
- app_name(名前空間)を設定する


#### 3. Userモデルを拡張する

デフォルトで提供されるUserモデルには以下のフィールドがある。

<a href="https://docs.djangoproject.com/en/3.2/ref/contrib/auth/" target="_blank">django.contrib.auth</a>

class models.User

|field|
|---|
|username|
|first_name|
|last_name|
|email|
|password|
|groups|
|user_permissions|
|is_staff|
|is_active|
|is_superuser|
|last_login|
|date_joined|


デフォルトのフィールド以外にも必要なフィールドがある場合は、拡張する必要がある。拡張する方法はおもに以下の3つ。

1. 抽象クラスAbstractBaseUserを継承する -> リリース前でガラッと変えたいならこれ
2. 抽象クラスAbstractUserを継承する -> リリース前でチョロっと追加したいならこれ
3. 別モデルを作ってOneToOneFieldで関連させる -> リリース後ならこれ


ex: AbstractUserを継承する場合

1. Edit accounts/models.py
2. Edit config/settings.py

```python[accounts/models.py]
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
  class Meta:
    db_table = 'custom_user'

  login_count = models.IntegerField(varbose_name='ログイン回数', default=0)
```

```python[settings.py]
AUTH_USER_MODEL = 'accounts.CustomUser' # <アプリケーション名>.<モデルクラス名>
```


#### 4. 発行されるクエリを確認する

オブジェクトの検索が実行されるときにどのようなクエリが発行されるか　ーモデルの使い方は合っているか？パフォーマンスに影響はないか？ー　確認する。

1. Djangoシェルを使う
2. ロギングの設定を変更する
3. django-debug-toolbarのSQLパネルを使う(後述)


#### 5. selected_related / prefetch_relatedでクエリ本数を減らす

N+1問題を回避する。モデルでリレーション先のデータを取得するときに使う。

|METHOD|NOTE|
|---|---|
|selected_related|「一」や「多」側から「一」のオブジェクトをJOINで取得|
|prefetch_related|「一」や「多」側から「多」のオブジェクトを取得してキャッシュに保持|

```python
Book.objects.all().select_related('publisher')
SELECT * FROM book INNER JOIN publisher ON book.publisher_id = publisher.id
```

```python
Book.objects.all().prefetch_related('authors')
```

#### 6. ベーステンプレートを用意する

テンプレートの共通部分　ーheadタグやbodyタグ終了前のJavaScriptー　をbase.htmlに分割する。

```bash
`-- templates
    |-- accounts
    |   `-- login.html
    `-- base.html
```


#### 7. こんなときはModelFormを継承しよう

通常のフォームが継承しているdjango.forms.Formの代わりにdjango.forms.models.ModelFormを継承することで特定のモデルのフィールド定義を再利用できる。デフォルトのフォームバリデーションの他にモデルのバリデーションが走る。

```python[accounts/forms.py]
from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ('username', 'email', 'password',)
    widgets = {
      'password': forms.PasswordInput(attrs={'placeholder': 'パスワード'}),
    }
  password_confirm = forms.CharField(
    label='パスワード確認',
    required=True,
    strip=False,
    widget=forms.PasswordInput(attrs={'placeholder': 'パスワード確認'}),
  )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget.attrs = {'placeholder': 'ユーザー名'}
    self.fields['email'].required = True
    self.fields['email'].widget.attrs = {'placeholder': 'メールアドレス'}

  # ユニーク制約チェック
  def clean(self):
    super().clean()
    password = self.cleaned_data['password']
    password_confirm = self.cleaned_data['password_confirm']
    if password != password_confirm:
      raise forms.ValidationError('パスワードとパスワード確認が合致しません')
```

```python[accounts/views.py]
form = RegisterForm(request.POST)
# save
user = form.save()
# or
user = form.save(commit=False)
user.set_password(form.cleaned_data['password'])
user.save()
```


#### 8. メッセージフレームワークを使う


## Setup environment

1. Make Pipfile
2. Install pipenv and packages

```bash[bash]
cd app
pip install pipenv
pipenv install
pipenv shell
(app) django-admin.py startproject config .
(app) python manage.py migrate
(app) python manage.py runserver
```

## Setup docker

1. Make Dockerfile for Django
2. Make dokcer-compose.yml for Django

## Update settings.py

1. SECRET_KEY
2. DEBUG
3. ALLOWED_HOSTS

## Start via docker-compose

```bash[bash]
docker-compose up -d --build
```

## Setup postgres

1. Add postgres service in docker-compose.yml
2. Update .env for postgresql
3. Update settings.py
4. Update Dockerfile for psycopg2

Up docker-compose and migrate. So we can see welcome page on localhost:8000.

```bash[bash]
docker-compose down -v
docker-compose up -d --build
docker-compose exec django python manage.py migrate
```

### Setup auto migrate

1. Add entrypoint.sh
2. chmod +x entrypoint.sh
3. Update Dockerfile

```bash[bash]
chmod +x app/entrypoint.sh
```


## Setup Gunicorn

1. Add gunicorn in Pipfile
2. Add docker-compose.prod.yml and update
3. Add entrypoint.prod.sh
4. Add Dockerfile.prod
5. Update docker-compose.prod.yml for new Dockerfile.prod
6. CMD and check localhost:8000/admin

```bash[bash]
docker-compose down -v
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec django python manage.py migrate --noinput
```


## Setup Nginx

1. Make nginx dir to root
2. Add Dockerfile
3. Add nginx.conf
4. Add nginx in docker-compose.prod.yml
5. Check connection of nginx

```bash[bash]
docker-compose down -v
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec django python manage.py migrate --noinput
```


## Setup static file

1. Update settings.py
2. Update entrypoint.sh for collectstatic command
3. Update docker-compose.prod.yml for staticfiles
4. Update nginx.conf for staticfiles

```bash[bash]
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec django python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec django python manage.py collectstatic
```
