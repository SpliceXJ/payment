import os
import uuid
from django.db import models
from cryptography.fernet import Fernet
from django.contrib.auth.models import User

fernet = Fernet(bytes(os.getenv("ENCRYPTION_KEY")))

class SpliceUser(User):
    """username field houses the ID of the user generated on the Node JS application"""

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_vendor = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_id = models.BinaryField()

    def __str__(self) -> str:
        return self.username

    @staticmethod
    def creare(email: str, username: str) -> "SpliceUser":
        return SpliceUser.objects.create(
            username=username,
            email=email,
            transaction_id=SpliceUser.encrypt_id(uuid.uuid4()),
            password=str(uuid.uuid4())[:10],
        )

    @staticmethod
    def encrypt_id(transaction_id: uuid.uuid4) -> bytes:
        return fernet.encrypt(transaction_id.encode())

    def get_transaction_id(self) -> uuid.UUID:
        # decrypt transaction id and return
        """ if database is local, Binary is stord as type Bytes else type Memory View """
        return (
            fernet.decrypt(self.transaction_id).decode() if os.getenv("ENVIROMENT") == "LOCAL"
            else 
            fernet.decrypt(self.transaction_id.tobytes()).decode()
            )
