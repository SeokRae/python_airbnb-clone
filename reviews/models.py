from django.db import models
from core import models as core_models

# Create your models here.


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    review = models.TextField()
    accuracy = models.IntegerField(default=0)
    communication = models.IntegerField(default=0)
    cleanliness = models.IntegerField(default=0)
    location = models.IntegerField(default=0)
    check_in = models.IntegerField(default=0)
    value = models.IntegerField(default=0)
    # 유저 삭제 시 숙소도 삭제
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    # 숙소 삭제 시 하위 테이블 데이터도 삭제
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        # python3 String 쓰는 방식
        return f"{self.review} - {self.room}"

    def rating_average(self):
        avg = (
            self.accuracy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)

    rating_average.short_description = "Avg."
