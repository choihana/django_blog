from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

class Contact(models.Model):
    user_from = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        indexed = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']
    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


user_model = get_user_model()
#symmetrical -> 내가 팔로우했을때 상대가 자동으로 나를 팔로우하지 않도록 False값으로 설정
user_model.add_to_class(
    'following',
    models.ManyToManyField(
        'self', through=Contact, related_name='followers', symmetrical=False
    )
)