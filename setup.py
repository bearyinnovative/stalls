from setuptools import setup, find_packages


install_required = [l.strip() for l in open("requirements.txt", "r")]


metadata = {'name': 'bearychat-apps-vote',
            'version': '0.1',
            'packages': find_packages(),
            'author': 'shonenada',
            'author_email': 'shonenada@gmail.com',
            'url': "https://github.com/shonenada/bearychat-apps-vote",
            'zip_safe': False,
            'platforms': ['linux'],
            'install_requires': install_required,
            'description': 'Vote Robot for BearyChat'}


if __name__ == '__main__':
    setup(**metadata)
