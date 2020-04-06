from django import template
from lists import models as list_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, room):
    user = context.request.user
    # 비 로그인 user 처리
    if user.is_anonymous:
        return False

    the_list = list_models.List.objects.get_or_none(
        user=user, name="My Favourites Houses"
    )

    if the_list is not None:
        return room in the_list.rooms.all()

    return False
