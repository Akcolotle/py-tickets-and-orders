from db.models import Order, Ticket, User
from django.db import transaction
import datetime

@transaction.atomic
def create_order(tickets, username, date=None):
    user = User.objects.get(username=username)
    if date:
        if isinstance(date, str):
            parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        else:
            parsed_date = date
        order = Order.objects.create(user=user)
        Order.objects.filter(id=order.id).update(created_at=parsed_date.replace(tzinfo=None))
        order.refresh_from_db()
    else:
        order = Order.objects.create(user=user)

    for t in tickets:
        Ticket.objects.create(
            movie_session_id=t["movie_session"],
            order=order,
            row=t["row"],
            seat=t["seat"]
        )
    return order



def get_orders(username=None):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
