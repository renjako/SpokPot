from distutils.core import setup

setup(
        name = 'SpokPot',
        packages = ['spokpot'],
        version = '0.1',
        description = 'Simple Python just OK Honeypot',
        author = 'Aldo Alase',
        author_email = 'aldoalase@gmail.com',
        url = 'https://github.com/aldoalase/SpokPot',
#        download_url = '',
        keywords = ['honeypot'],
        classifiers = [
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Development Status :: Pre-alpha',
        ],
        long_description = 'Honeypot for final project that emulate RFI, LFI and some GHDB'
)
