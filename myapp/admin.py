from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'password', 'phone', "role", "status","id_proof")
    search_fields = ('name', 'email')

@admin.register(Contact_detail)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message', 'timestamp')

@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'date_of_birth', 'profession','bio','user_image')

@admin.register(AuthorProfile)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'biography', 'total_books_published', "years_of_experience", "specialization","author_image")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'description', 'category', "subscription_type", 'book_image', "created_at")

@admin.register(BookFile)
class BookFileAdmin(admin.ModelAdmin):
    list_display = ('author','book', 'file', 'uploaded_at')

@admin.register(BookPublishRequest)
class PublishAdmin(admin.ModelAdmin):
    list_display = ('book', 'publisher', 'publish_date', 'additional_notes', 'status', 'created_at')


@admin.register(Plan)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_type', 'price', 'duration_months', 'description',
                    'max_books_per_month', 'can_listen_audio','created_at','updated_at', 'is_active'
                    )

@admin.register(PlanOrder)
class PlanorderAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature','amount','status','purchase_date','expiration_date')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user','book','ratings','comment','timestamp')

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('user','subject','description','timestamp')