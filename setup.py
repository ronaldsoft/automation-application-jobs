from setuptools import setup, find_packages

setup (
       name='getjob',
       version='1.0',
       packages=find_packages(),

       # Declare your packages' dependencies here, for eg:
       install_requires=['email', 'csv', 'json', 'smtplib', 'ssl'],
       author='Ronald Rivera',
       author_email='ronaldsoft8423@gmail.com',
       url='https://github.com/ronaldsoft/getjob',
       long_description='This code is to send mails with different context depending of company info.',
       include_package_data=True,
      )