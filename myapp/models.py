from django.db import models
from django.utils.safestring import mark_safe
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta  # Use this for month-based delta
# Create your models here.

class Login(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, default="admin@123")
    phone = models.CharField(max_length=50, null=True, blank=True)

    ROLE = (
        ("Publisher", "Publisher"),
        ("Author", "Author"),
        ("User", "User"),
    )
    role = models.CharField(max_length=30, choices=ROLE, default='User')

    STATUS = (
        ("0", "unapproved"),
        ("1", "approved")
    )
    status = models.CharField(max_length=10, choices=STATUS, default='0')

    id_proof = models.FileField(upload_to='id_proofs/', null=True, blank=True, default=None)

    def pic(self):
        return mark_safe('<img src = "{}" width = "100">'.format(self.id_proof.url))
    pic.allow_tags = True

    def __str__(self):
        return self.name

class Contact_detail(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=30)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    address = models.TextField()
    date_of_birth = models.DateField(blank=True, null=True)
    profession = models.CharField(max_length=100)  # User's profession
    bio = models.TextField(blank=True, null=True)  # Brief introduction
    userprofile_image = models.ImageField(upload_to='media/', blank=True, null=True)

    def user_image(self):
        return mark_safe('<img src = "{}" width = "100">'.format(self.userprofile_image.url))
    user_image.allow_tags = True

    def __str__(self):
        return self.user.name

class AuthorProfile(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    total_books_published = models.PositiveIntegerField(default=0)
    years_of_experience = models.FloatField(blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='author_profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.name

    def author_image(self):
        return mark_safe('<img src = "{}" width = "100">'.format(self.profile_picture.url))
    author_image.allow_tags = True

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# Book Model
class Book(models.Model):
    SUBSCRIPTION_TYPES = (
        ('Free', 'Free'),
        ('Premium', 'Premium'),
    )
    author = models.ForeignKey('Login', on_delete=models.CASCADE, limit_choices_to={'role': 'Author'}, default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPES)
    book_image = models.ImageField(upload_to='media/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def book_pic(self):
        return mark_safe('<img src = "{}" width = "100">'.format(self.book_image.url))
    book_pic.allow_tags = True

class BookFile(models.Model):
    author = models.ForeignKey('Login', on_delete=models.CASCADE, limit_choices_to={'role': 'Author'}, default='')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(
        upload_to='books/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'epub', 'mp3', 'wav', 'aac'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for {self.book.title}"

class BookPublishRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="publish_requests")
    publisher = models.ForeignKey('Login', on_delete=models.CASCADE, limit_choices_to={'role': 'Publisher'})
    publish_date = models.DateField()
    additional_notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for {self.book.title} by {self.publisher.name} ({self.status})"

class Plan(models.Model):
    PLAN_TYPE_CHOICES = [
        ('Standard', 'Standard'),
        ('Premium', 'Premium'),
    ]

    name = models.CharField(max_length=100)  # e.g., Standard, Ultimate
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.IntegerField()
    description = models.TextField()
    max_books_per_month = models.IntegerField(default=0, help_text="Number of books a user can access per month")
    can_listen_audio = models.BooleanField(default=False)  # If the user can listen to audiobooks
    created_at = models.DateTimeField(auto_now_add=True)  # Date the plan was added
    updated_at = models.DateTimeField(auto_now=True)  # Last update time
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User

class PlanOrder(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Failed', 'Failed')], default='Pending')
    purchase_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    expiration_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Ensure purchase_date is set before calculating expiration_date
        if not self.expiration_date and self.purchase_date:
            self.expiration_date = self.purchase_date + relativedelta(months=self.plan.duration_months)
        super().save(*args, **kwargs)

        if self.status == 'Paid':
            self.plan.is_active = True
            self.plan.save()

    def is_active(self):
        # Check if the current date is before the expiration date
        return self.expiration_date and self.expiration_date > timezone.now()

    def __str__(self):
        return f"Order {self.razorpay_order_id} by {self.user}"

class Feedback(models.Model):
    user = models.ForeignKey('Login', on_delete=models.CASCADE, default="")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    ratings = models.IntegerField()
    comment = models.CharField(max_length=300, default="")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback from {self.user.name}"

class Complaint(models.Model):
    user = models.ForeignKey('Login', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Complaint from {self.user.name} - {self.subject}"