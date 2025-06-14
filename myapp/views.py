from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *

# Create your views here.
def checksession(request):
    uid = request.session.get('log_id')

    if not uid:
        return None

    try:
        userdata = Login.objects.get(id=uid)
        is_author = userdata.role == "Author"
        is_publisher = userdata.role == "Publisher"


        if is_author:
            try:
                profile = AuthorProfile.objects.get(user=userdata)
            except AuthorProfile.DoesNotExist:
                profile = None
        else:
            try:
                profile = UserProfile.objects.get(user=userdata)
            except UserProfile.DoesNotExist:
                profile = None

        user_has_paid_plan = PlanOrder.objects.filter(user=userdata, status='Paid').exists()

        context = {
            'userdata': userdata,
            'is_author': is_author,
            'is_publisher': is_publisher,
            'profile': profile,
            'user_has_paid_plan': user_has_paid_plan,  # Add the paid plan status to the context
        }
        return context
    except Login.DoesNotExist:
        return None


def index(request):
    context = checksession(request)
    if context is None:
        context = {}
    categories = Category.objects.all()
    context['alldepartments'] = categories
    return render(request,'index.html',context)

def about(request):
    context = checksession(request)
    return render(request,'about-us.html',context)

def contact(request):
    context = checksession(request)
    if request.method == "POST":
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Subject = request.POST.get('subject')
        Message = request.POST.get('message')

        if Contact_detail.objects.filter(email=Email).exists():
            messages.error(request, 'You have already filled out contact details.')
            return redirect('contact')  # Assuming you have a URL pattern named 'contact1'
        else:
            contactdata = Contact_detail(name=Name, email=Email, subject=Subject, message=Message)
            contactdata.save()
            messages.success(request, 'Your contact details have been saved.')
            return redirect('index')  # Ensure 'index' is the name of your URL pattern or view function

    return render(request,'contact-us.html',context)

def find_products(request):
    context = checksession(request)
    if context is None:
        context = {}

    categories = Category.objects.all()
    # Get selected property type if any
    category_type = request.GET.get('category_type')
    products = Book.objects.all()
    if category_type:
        products = products.filter(category__id=category_type)

    context['bookdetails'] = products
    context['alldepartments'] = categories
    return render(request, 'books.html', context)

def book(request):
    context = checksession(request)
    if context is None:
        context = {}

    # Check if the user has a paid plan
    user_has_paid_plan = context.get('user_has_paid_plan', False)

    # Filter books based on subscription status
    if user_has_paid_plan:
        allbooks = Book.objects.all()  # Show both Free and Premium books
    else:
        allbooks = Book.objects.filter(subscription_type='Free')  # Show only Free books

    context['bookdetails'] = allbooks
    return render(request, 'books.html', context)

def bookdetail(request,bid):
    context = checksession(request)
    bookdetails = Book.objects.get(id=bid)
    book_files = BookFile.objects.filter(book=bookdetails)  # Fetch all related files
    context.update({'bookdetails':bookdetails,'book_files': book_files})
    return render(request,'books-detail.html',context)

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name1')
        email = request.POST.get('email1')
        password = request.POST.get('password1')
        phone = request.POST.get('phone1')
        role = request.POST.get('usertype')

        # Create a new Login object
        new_user = Login(name=name, email=email, password=password, phone=phone, role=role)

        # Check if id_proof1 exists in request.FILES
        if 'id_proof1' in request.FILES:
            id_proof = request.FILES['id_proof1']
            new_user.id_proof = id_proof

        # Save user based on their role
        if role == 'User':
            messages.info(request, 'Registration done successfully. Please wait for your profile approval. It will take around 2-3 days.')
        else:
            messages.success(request, 'Data inserted successfully. You can login now.')

        new_user.save()

        # Redirect to a success page
        return redirect('/')

    return render(request,'signup.html')

def login(request):
    if request.method == "POST":
        Email1 = request.POST['email2']
        Password1 = request.POST['password2']
        try:
            user = Login.objects.get(email=Email1, password=Password1)

        except Login.DoesNotExist:
            user = None

        if user is not None:
            if user.role == "User" and user.status == "0":
                print(user.role)
                print(user.status)
                messages.error(request, 'Your Profile is Under Approval Process. This may take upto 3 working days.')
            else:
                request.session['log_id'] = user.id
                request.session.save()
                messages.success(request, 'Login successful...')
                return redirect('/')
        else:
            messages.error(request, 'Invalid Email Id and Password. Please try again.')
            return redirect('/login')

    return render(request,'login_page.html')

def logout(request):
    try:
        del request.session['log_id']
        messages.success(request,'your logout successfully.')
        return redirect(index)
    except:
        pass
    return render(request,'index.html')

def forgotpassword(request):
    if request.method == 'POST':
        username = request.POST.get('email2')
        try:
            user = Login.objects.get(email=username)

        except Login.DoesNotExist:
            user = None
        # if user exist then only below condition will run otherwise it will give error as described in else condition.
        if user is not None:
            #################### Password Generation ##########################
            import random

            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                       'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

            nr_letters = 6
            nr_symbols = 1
            nr_numbers = 3
            password_list = []

            for char in range(1, nr_letters + 1):
                password_list.append(random.choice(letters))

            for char in range(1, nr_symbols + 1):
                password_list += random.choice(symbols)

            for char in range(1, nr_numbers + 1):
                password_list += random.choice(numbers)

            print(password_list)
            random.shuffle(password_list)
            print(password_list)

            password = ""  # we will get final password in this var.
            for char in password_list:
                password += char

            ##############################################################

            msg = "hello here it is your new password  " + password  # this variable will be passed as message in mail

            ############ code for sending mail ########################

            from django.core.mail import send_mail

            send_mail(
                'Your New Password',
                msg,
                'parthinfolabz19@gmail.com',
                [username],
                fail_silently=False,
            )
            # NOTE: must include below details in settings.py
            # detail tutorial - https://www.geeksforgeeks.org/setup-sending-email-in-django-project/
            # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
            # EMAIL_HOST = 'smtp.gmail.com'
            # EMAIL_USE_TLS = True
            # EMAIL_PORT = 587
            # EMAIL_HOST_USER = 'mail from which email will be sent'
            # EMAIL_HOST_PASSWORD = 'pjobvjckluqrtpkl'   #turn on 2 step verification and then generate app password which will be 16 digit code and past it here

            #############################################

            # now update the password in model
            cuser = Login.objects.get(email=username)
            cuser.password = password
            cuser.save(update_fields=['password'])

            print('Mail sent')
            messages.info(request, 'mail is sent')
            return redirect(index)

        else:
            messages.info(request, 'This account does not exist')
        return redirect(index)

def adduserdetail(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == "POST":
        Address = request.POST.get('address')
        Profile_image = request.FILES.get('profile_image')
        Dob = request.POST.get('date_of_birth')
        Profession = request.POST.get('profession')
        bio = request.POST.get('bio')

        userdata = UserProfile(user=Login(id=uid), address=Address,userprofile_image=Profile_image,date_of_birth=Dob, profession=Profession, bio=bio)
        userdata.save()
        messages.success(request, 'your profile data is saved.')
        return redirect(index)
    return render(request,'adduser.html', context)

def showuser(request):
    context = checksession(request)
    uid = request.session['log_id']
    alluserdetails = UserProfile.objects.get(user=Login(id=uid))
    context.update({
        'alldetail': alluserdetails,
    })
    return render(request,'showuser.html', context)

def editprofile(request):
    context = checksession(request)
    uid = request.session['log_id']
    edituser = UserProfile.objects.get(user=Login(id=uid))
    context.update({
        'data': edituser,
    })
    return render(request,'edituserdetail.html',context)

def update(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == "POST":
        Address = request.POST.get('address1')
        Dob = request.POST.get('date_of_birth1')
        profession = request.POST.get('profession1')
        bio = request.POST.get('bio1')
        object = UserProfile.objects.get(user=uid)
        object.address=Address
        object.date_of_birth=Dob
        object.profession=profession
        object.bio=bio

        if 'profile_image1' in request.FILES:
            file = request.FILES['profile_image1']
            object.userprofile_image = file
        object.save()
        messages.success(request, 'your profile has been completed..')

        return redirect('/showuser')
    return render(request,'edituserdetail.html',context)

def addauthor(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == "POST":
        Address = request.POST.get('address')
        Profile_image = request.FILES.get('sellerprofile_image')
        biography = request.POST.get('biography')
        total_books_published = request.POST.get('published_book')
        yoe = request.POST.get('years_of_experience')
        spec = request.POST.get('specialization')

        userdata = AuthorProfile(user=Login(id=uid), address=Address, profile_picture=Profile_image, biography=biography, total_books_published=total_books_published, years_of_experience=yoe, specialization=spec)
        userdata.save()
        messages.success(request, 'your profile data is saved.')
        return redirect(index)
    return render(request,'addauthor.html', context)

def showauthor(request):
    context = checksession(request)
    uid = request.session['log_id']
    allsellerdetails = AuthorProfile.objects.get(user=Login(id=uid))
    context.update({
        'sellerdetail': allsellerdetails,
    })
    return render(request,'showauthor.html', context)

def editauthor(request):
    context = checksession(request)
    uid = request.session['log_id']
    editseller = AuthorProfile.objects.get(user=Login(id=uid))
    context.update({
        'data': editseller,
    })
    return render(request,'editauthordetail.html',context)

def updateauthor(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == "POST":
        Address = request.POST.get('address2')
        shop = request.POST.get('shop_name2')
        saddress = request.POST.get('shop_address2')
        yearofexp = request.POST.get('years_of_experience2')
        speci = request.POST.get('specialization2')
        rat = request.POST.get('ratings2')
        avail = request.POST.get('availability2')
        object = AuthorProfile.objects.get(user=uid)
        object.address=Address
        object.shop_name=shop
        object.shop_address=saddress
        object.years_of_experience=yearofexp
        object.specialization=speci
        object.rating=rat
        object.availability=avail

        if 'seller1' in request.FILES:
            file = request.FILES['seller1']
            object.sellerprofile_image = file
        object.save()
        messages.success(request, 'your profile has been completed..')

        return redirect('/showseller')
    return render(request,'editauthordetail.html',context)

def upload_book(request):
    context = checksession(request)
    profile6 = context.get("profile")
    print(profile6)

    if profile6 == None:
        messages.error(request, "please complete your profile.")
        return redirect('addauthor')

    uid = request.session['log_id']
    if request.method == "POST":
        title = request.POST['title']
        category_id = request.POST['category']
        description = request.POST['description']
        subscription_type = request.POST['subscription_type']
        book_image = request.FILES.get('book_image')

        category = Category.objects.get(id=category_id)

        Book.objects.create(
            author=Login(id=uid),
            category=category,
            title=title,
            description=description,
            subscription_type=subscription_type,
            book_image=book_image,
        )
        return redirect('index')  # Redirect to book list after upload

    categories = Category.objects.all()
    context.update({'categories': categories})
    return render(request, 'addbook.html', context)

def upload_book_detail(request):
    context = checksession(request)
    profile6 = context.get("profile")
    print(profile6)

    if profile6 == None:
        messages.error(request, "please complete your profile.")
        return redirect('addauthor')

    uid = request.session['log_id']
    if request.method == "POST":
        category_id = request.POST['category']
        file = request.FILES.get('file')

        category = Book.objects.get(id=category_id)

        BookFile.objects.create(
            author=Login(id=uid),
            book=category,
            file=file,

        )
        return redirect('index')  # Redirect to book list after upload

    categories = Book.objects.all()
    context.update({'categories': categories})
    return render(request, 'add_book_detail.html', context)

def send_publish_request(request):
    context = checksession(request)

    uid = request.session['log_id']
    if request.method == "POST":
        category_id = request.POST['category']
        description = request.POST['description']
        date = request.POST['date']

        category = Book.objects.get(id=category_id)

        BookPublishRequest.objects.create(
            publisher=Login(id=uid),
            book=category,
            additional_notes=description,
            publish_date=date,
            status="Pending",

        )
        return redirect('index')  # Redirect to book list after upload

    categories = Book.objects.all()
    context.update({'categories': categories})
    return render(request, 'addpublishrequest.html', context)

def update_publisher_request(request):
    context = checksession(request)
    """ View for Service Providers to see and manage their bookings. """
    provider_id = request.session.get('log_id')  # Get logged-in service provider ID

    # Fetch only bookings related to the services added by the service provider
    bookings = BookPublishRequest.objects.filter(book__author_id=provider_id)

    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        action = request.POST.get("action")  # 'accept' or 'reject'

        booking = get_object_or_404(BookPublishRequest, id=booking_id)

        if action == "accept":
            booking.status = "Approved"
        elif action == "reject":
            booking.status = "Rejected"

        booking.save()
        return redirect("update_publisher_request")  # Reload the page after action

    context.update({"bookings": bookings})

    return render(request, "view_request.html", context)


def showrequest(request):
    context = checksession(request)
    uid = request.session['log_id']
    bookings = BookPublishRequest.objects.filter(publisher_id=uid)
    context.update({"bookings": bookings})
    return render(request,'showrequest.html', context)
def pricing(request):
    context = checksession(request)
    user_id = request.session['log_id']
    user = Login.objects.get(id=user_id)

    # Fetch all active plans (with Paid status)
    active_plan_orders = PlanOrder.objects.filter(user=user, status='Paid')
    active_plan_ids = active_plan_orders.values_list('plan_id', flat=True)

    # Update active status of plans based on paid orders
    Plan.objects.filter(id__in=active_plan_ids).update(is_active=True)

    # Fetch all available plans
    plans = Plan.objects.all()

    context.update({
        'plans': plans,
        'active_plan_ids': list(active_plan_ids),  # Convert to list if necessary
    })

    return render(request,'pricing.html', context)

import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Plan
from django.utils import timezone

def create_order(request, plan_id):
    uid = request.session['log_id']
    plan = Plan.objects.get(id=plan_id)

    # Check if the user already has an active plan
    active_order = PlanOrder.objects.filter(user_id=uid, status='Paid').filter(
        expiration_date__gt=timezone.now()).first()

    if active_order:
        messages.error(request, "You already have an active plan. You cannot purchase another one.")
        return redirect('pricing')  # Redirect to the pricing page or wherever you prefer

    # Initialize Razorpay client
    razorpay_client = razorpay.Client(auth=('rzp_test_VQhEfe2NCXbbwI', '2ibreCYL78DA3kjOhobCvz0f'))

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create({
        "amount": int(plan.price * 100),  # Amount in paisa
        "currency": "INR",
        "payment_capture": '1',  # Auto-capture payment after successful
        "receipt": f"order_{uid}",
    })
    # Save Order in your DB (You should have an Order model to track)
    order = PlanOrder.objects.create(
        plan=plan,
        user=Login(id=uid),
        razorpay_order_id=razorpay_order['id'],
        amount=plan.price
    )
    print(razorpay_order)
    order.save()

    context = {
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key_id': 'rzp_test_VQhEfe2NCXbbwI',
        'amount': plan.price,
        'currency': 'INR',
        'plan': plan,
    }

    return render(request, 'payment_page.html', context)

from django.core.mail import send_mail
from django.shortcuts import render, redirect
import razorpay

def payment_success(request):
    if request.method == 'POST':
        # Extract the Razorpay response details from the POST request
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_signature = request.POST.get('razorpay_signature', '')

        if not razorpay_order_id or not razorpay_payment_id or not razorpay_signature:
            # Handle missing information
            return render(request, 'failure.html', {'status': 'Error: Missing payment details'})

        # Verify the payment signature with Razorpay
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature,
        }

        try:
            client = razorpay.Client(auth=('rzp_test_VQhEfe2NCXbbwI', '2ibreCYL78DA3kjOhobCvz0f'))
            client.utility.verify_payment_signature(params_dict)

            # Fetch the PlanOrder and update its status
            plan_order = PlanOrder.objects.get(razorpay_order_id=razorpay_order_id)
            plan_order.razorpay_payment_id = razorpay_payment_id
            plan_order.razorpay_signature = razorpay_signature
            plan_order.status = 'Paid'
            plan_order.save()

            subject = 'Payment Successful'
            message = f"Dear {plan_order.user.name},\n\n" \
                      f"Thank you for purchasing the {plan_order.plan.name} plan. Your payment was successful! \n\n" \
                      f"Best regards,\nYour Team"
            sender_email = 'dpoza8125@gmail.com'  # Replace with your sender email address
            recipient_email = [plan_order.user.email]

            send_mail(subject, message, sender_email, recipient_email, fail_silently=False)


            # Payment was successful
            return render(request, 'success.html', {'status': True})

        except razorpay.errors.SignatureVerificationError:
            # Handle invalid signature
            return render(request, 'failure.html', {'status': 'Signature verification failed.'})

        except PlanOrder.DoesNotExist:
            # Handle invalid order
            return render(request, 'failure.html', {'status': 'Order does not exist.'})

        except Exception as e:
            # Handle any other errors
            return render(request, 'failure.html', {'status': f"Error: {str(e)}"})

def showfeedback(request):
    context = checksession(request)
    uid = request.session.get('log_id')  # Ensure user is logged in and has a session
    books = Book.objects.all()
    if request.method == 'POST':
        product_id = request.POST.get('orders')  # Plant ID from the form
        ratings = request.POST.get('ratings')
        feedback_message = request.POST.get('feedback_message')

        # Create feedback if all checks pass
        Feedback.objects.create(
            user=Login.objects.get(id=uid),
            book=Book.objects.get(id=product_id),
            ratings=ratings,
            comment=feedback_message,
        )
        messages.success(request, "Your feedback has been submitted successfully.")
        return redirect('index')
    context.update({'bookdetails':books})
    return render(request, 'feedback.html', context)

def complaint_submit(request):
    context = checksession(request)
    uid = request.session['log_id']

    if request.method == "POST":
        sub = request.POST.get('subject1')
        desc = request.POST.get('description1')

        complaindata = Complaint(user=Login(id=uid),subject=sub, description=desc)
        complaindata.save()
        messages.success(request ,'your complain has been sent successfully.')
        return redirect('/')

    return render(request, 'Complaint.html', context)

