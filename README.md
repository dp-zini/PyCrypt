# PyCrypt

PyCrypt provides a simple way to encrypt, decrypt, and delete files in the CLI. 

## Key Features
- Quickly secure delete files and directories by overwriting the data.
- Support for custom passphrases.
- Encrypt and decrypt files and directories seamlessly.

## Installation
PyRSA uses pycryptodome for encryption and decryption.

``` python
pip install pycryptodome
```
## Usage
``` python
$ python pycrypt.py
```
From the CLI:
- Input filepath or drag onto script
- Select encryption, decryption or deletion
- Watch the magic!

## Warning
This was hacked out in like a day, there are some minor safeguards to prevent deleting the home dir, but you use it at your own risk, I'm not responsible for any lost data.

## Contributions
Feel free to contribute! There's probably some blatant security flaws in this lol, so take the code, edit it, use it in your own projects, do whatever! Just give proper attribution.

## License
Licensed under the MIT License, for more info see [LICENSE](https://github.com/dp-zini/PyCrypt/blob/main/LICENSE)
