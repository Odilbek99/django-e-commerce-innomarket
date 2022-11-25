from django import template

register = template.Library()

@register.simple_tag
def call_sellprice(price, discount):
    if discount == None or discount == 0:
        return price
    sellprice = price
    sellprice = price - (price * discount)/100
    return int(sellprice)

@register.simple_tag
def progress_bar(total_quantity, availability):
    progress_bar = availability
    progress_bar = availability * (100/total_quantity)
    return int(progress_bar) 