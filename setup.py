from distutils.core import setup
setup(
  name = 'aws-ping-login',
  py_modules = ['aws_ping_login'],
  entry_points = {
    'console_scripts': ['aws-ping-login=aws_ping_login:main'],
  },
  install_requires=[
        'boto3',
        'awscli',
        'wxPython',
        'bs4'
    ],
  description = 'aws-ping-login is a command line tool supporting logging in to AWS profiles using a Ping SSO website',
  version = '0.10.108',
  author = 'Mark Sweat',
  author_email = 'mark@surfkansas.com',
  url = 'https://github.com/surfkansas/aws-ping-login', 
  download_url = 'https://github.com/surfkansas/aws-ping-login/archive/0.10.108.tar.gz'
)