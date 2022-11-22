from django.template.context_processors import request

# from . import models


def shopping_cart(request):

    if request.user.is_authenticated:
        pass
    else:

        cart = dict()
        cart_dic = []
        if "cart" in request.session:
            cart_session = request.session["cart"]
            cart_price_total = 0
            for cart_ in cart_session:
                for c in cart_session[cart_]:
                    cart_dic.append(c)
                    cart_price_total += float(c["book_price"]) * float(
                        c["book_quantity"]
                    )

            cart["cart"] = cart_dic
            cart["cart_total"] = len(cart_dic)
            cart["cart_price_total"] = cart_price_total

            # create single dict
            # print(len(cart_dic))
            return cart
        else:
            cart["cart"] = None
            return cart
