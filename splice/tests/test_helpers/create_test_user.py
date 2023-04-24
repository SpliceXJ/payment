from faker import Faker

from splice.users.models.user import SpliceUser


def create_test_splice_user() -> "SpliceUser":
    import uuid

    return SpliceUser.create(email=Faker().email(), username=str(uuid.uuid4())[:20])
