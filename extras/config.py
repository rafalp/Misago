from django.utils.six.moves import configparser


yapf = configparser.ConfigParser()
yapf.read('.style.yapf')
