from django.http import Http404
from django.shortcuts import redirect, reverse, render
from django.views.generic import View
from users import models as user_models
from reservations import models as reservation_models
from . import models

# Create your views here.


def go_conversation(request, reservation_pk, host_pk, guest_pk):
    host = user_models.User.objects.get_or_none(pk=host_pk)
    guest = user_models.User.objects.get_or_none(pk=guest_pk)
    reservation = reservation_models.Reservation.objects.get_or_none(pk=reservation_pk)

    if host is not None and guest is not None:
        try:
            conversation = (
                models.Conversation.objects.filter(participants__pk=host_pk)
                & models.Conversation.objects.filter(participants__pk=guest_pk)
            ).first()

            if conversation is None:
                raise models.Conversation.DoesNotExist

        except models.Conversation.DoesNotExist:
            conversation = models.Conversation.objects.create(reservations=reservation)
            conversation.participants.add(host, guest)

    return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)

        if not conversation:
            raise Http404()
        return render(
            self.request,
            "conversations/conversation_detail.html",
            {"conversation": conversation},
        )

    def post(self, *args, **kwargs):
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        if message is not None:
            models.Message.objects.create(
                message=message, user=self.request.user, conversation=conversation
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))
