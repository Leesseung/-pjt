import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from products.models import DepositProducts, SavingProducts

def generate_membership_number():
    """
    Generate a unique 20-character membership number using UUID4.
    """
    return uuid.uuid4().hex[:20]

class UserSubscription(models.Model):
    """
    정기예금(DepositProducts) 구독 모델
    """
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='deposit_subscriptions'
    )
    product = models.ForeignKey(
        DepositProducts, on_delete=models.CASCADE
    )
    term_months = models.IntegerField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timezone.timedelta(days=self.term_months * 30)
        super().save(*args, **kwargs)

class SavingSubscription(models.Model):
    """
    적금(SavingProducts) 구독 모델
    """
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='saving_subscriptions'
    )
    product = models.ForeignKey(
        SavingProducts, on_delete=models.CASCADE
    )
    term_months = models.IntegerField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timezone.timedelta(days=self.term_months * 30)
        super().save(*args, **kwargs)

class User(AbstractUser):
    """
    Custom User model with profile fields and subscriptions.
    """
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio           = models.CharField(max_length=255, blank=True)
    age           = models.PositiveIntegerField(blank=True, null=True)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    salary          = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    membership_number = models.CharField(
        max_length=20, unique=True,
        default=generate_membership_number, editable=False
    )

    # Many-to-Many for subscribed products
    subscribed_deposit_products = models.ManyToManyField(
        DepositProducts, related_name='subscribers', blank=True
    )
    subscribed_saving_products = models.ManyToManyField(
        SavingProducts, related_name='subscribers_saving', blank=True
    )

    # 팔로우 기능: followers→나를 팔로우하는 사람들, related_name='following' gives 내가 팔로우하는 사람들
    followers = models.ManyToManyField(
        'self', symmetrical=False, related_name='following', blank=True
    )

    @property
    def active_subscriptions(self):
        now = timezone.now()
        deps = list(self.deposit_subscriptions.filter(end_date__gt=now))
        savs = list(self.saving_subscriptions.filter(end_date__gt=now))
        return deps + savs
