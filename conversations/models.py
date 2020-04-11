from django.db import models
from core import models as core_models
from django.urls import reverse

# Create your models here.


class Conversation(core_models.TimeStampedModel):

    """ Conversation Model Definition """

    # Conversation에 참여하는 사용자 Many To Many 필드
    participants = models.ManyToManyField(
        "users.User", related_name="conversations", blank=True
    )

    def __str__(self):
        usernames = []
        # 사용자간의 Conversation List를 갖고 와야 함
        for user in self.participants.all():
            usernames.append(user.username)
        return ", ".join(usernames)

    def count_messages(self):
        return self.messages.count()

    count_messages.short_description = "Number of Messages"

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "Number of Participants"

    def get_absolute_url(self):
        return reverse("conversations:detail", kwargs={"pk": self.pk})


class Message(core_models.TimeStampedModel):

    """ Message Model Definition """

    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"
