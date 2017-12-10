import os
import uuid

class SecretKey:
    def random_key(self):
        return os.urandom(24)
    def random_uid(self):
        return str(uuid.uuid4())
