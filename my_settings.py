#database 설정
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bibim',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

SECRET_KEY = 'django-insecure-aw0efor5oq-m%uds_t*sz81#8-gxbf6u+2@z^=mt@v_vjg)!1#'
