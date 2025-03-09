class Key:
    def __init__(self):
        self._passphrase = "zax2rulez"
        self._number = 9001
        self._str = "GeneralTsoKeycard"
        self._len = 1337
        self._item = 3

    @property
    def passphrase(self):
        return self._passphrase
    
    @passphrase.setter
    def passphrase(self, value):
        self._passphrase = value
    
    @passphrase.deleter
    def passphrase(self):
        del self._passphrase
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}(passpharse = {self._passphrase})"

    def __len__(self):
        return self._len

    def __str__(self):
        return self._str

    def __int__(self):
        return self._number

    def __getitem__(self, item):
        return self._item

    def __gt__(self, other):
        return self._number > other
