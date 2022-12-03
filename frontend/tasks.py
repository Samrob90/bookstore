from celery import shared_task
from . import models
from authentications.models import Account
from cpanel.models import book
from frontend.models import recent_viewied_item


@shared_task
def save_recent(pk, bookid, data):
    books = book.objects.filter(pk=bookid).first()
    # check if user id is not not (not auhtenticated)
    if pk is not None:
        user = Account.objects.filter(pk=pk)
        book_exist_in_recent_view = recent_viewied_item.objects.filter(
            user=user, product_id=books.pk
        )
        if book_exist_in_recent_view.exists():
            book_exist_in_recent_view.delete()
        else:
            recent_viewied_item.objects.create(**data)
    return "done"
