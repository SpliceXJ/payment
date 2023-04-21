from splice.users.models.user import SpliceUser
from splice.users.models.cards import UsersCard

# multiprocess this stuff in view:
def save_payment_card(data, owner_id):
    return UsersCard.create(
        owner=SpliceUser.objects.get(id=owner_id),
        authorization=data["authorization"]["authorization_code"],
        email=data["customer"]["email"],
        last_four_digits=data["authorization"]["last4"],
        card_type=data["authorization"]["card_type"]
    )
