from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import OTPVerification, User, Form
from .forms import EmailForm, OTPVerificationForm
from django.contrib import messages

@api_view(['GET'])
def index(request) :
    obj = {
        'api': 'hello',
        'items': ['mango', 'banana']
    }
    return Response(obj)

def signup_with_otp(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            
            # Generate new OTP and reference
            otp = OTPVerification.generate_otp()
            reference = OTPVerification.generate_reference()
            
            # Save OTP verification record
            OTPVerification.objects.create(
                email=user_email,
                otp=otp,
                reference_otp=reference,
            )
            
            # Send OTP via email
            try:
                send_mail(
                    'Your Sign Up OTP',         # EMAIL TEMPLATE
                    f'Your One-Time Password #{reference} is: {otp}\nIt will expire in 10 minutes.',
                    'xxxxxxxxxx@gmail.com',     # SENDER EMAIL
                    [user_email],
                    fail_silently=False,
                )
                print(f"OTP sent successfully to {user_email}")
            except Exception as e:
                print(f"Error sending email: {str(e)}")
                form.add_error(None, 'Error sending OTP email. Please try again.')
                return render(request, 'signup_with_otp.html', {'form': form})
            
            # Store email in session for verification
            request.session['email_for_otp'] = user_email
            return redirect('verify_otp')
    else:
        form = EmailForm()
    return render(request, 'signup_with_otp.html', {'form': form})

def verify_otp(request):
    user_email = request.session.get('email_for_otp')
    if not user_email:
        return redirect('signup_with_otp')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            
            # Check if OTP matches and is not expired
            otp_obj = OTPVerification.objects.filter(
                email=user_email,
                created_at__gte=timezone.now() - timedelta(minutes=10)      # OTP EXPIRATION TIME
            ).last()
            
            if len(entered_otp) != 6:  # ensure OTP is 6 characters
                messages.error(request, 'OTP must be exactly 6 digits')
                return render(request, 'verify_otp.html', {
                    'form': form,
                    'error': 'OTP must be exactly 6 digits'
                    })
            
            if otp_obj and (otp_obj.otp == entered_otp):
                # Email is verified
                request.session['verified_email'] = user_email
                
                # Clean up OTP verification records
                OTPVerification.objects.filter(email=user_email).delete()
                
                # Redirect to complete registration
                return redirect('complete_registration')
            else:
                messages.error(request, 'Invalid or expired OTP')
                return render(request, 'verify_otp.html', {
                    'form': form, 
                    'error': 'Invalid or expired OTP'
                })
    else:
        form = OTPVerificationForm()
    
    return render(request, 'verify_otp.html', {'form': form})

def complete_registration(request):
    verified_email = request.session.get('verified_email')
    if not verified_email:
        return redirect('signup_with_otp')
    
    if request.method == 'POST':
        # Get registration form data
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        name = request.POST.get('name')
        role = request.POST.get('role')
        student_code = request.POST.get('student-code')
        key_code = request.POST.get('key-code')
        
        # Validate form data
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'complete_registration.html', 
                        {'error': 'Passwords do not match'})                        # FRONTEND

        if role == 'student':           # FOR STUDENT
            if not student_code:
                messages.error(request, 'Student code is required for students')
                return render(request, 'complete_registration.html', 
                            {'error': 'Student code is required for students'})     # FRONTEND
            if User.objects.filter(student_code=student_code).exists():
                messages.error(request, 'Student code already exists')
                return render(request, 'complete_registration.html', 
                            {'error': 'Student code already exists'})               # FRONTEND

            
            # Create new student user
            user = User.objects.create(
                email=verified_email,
                password=password, 
                name=name,
                student_code=student_code,
                role=User.Role.STUDENT
            )
            # Create new form
            form = Form.objects.create(
                form_status=Form.FormStatus.DRAFT,
                form_type=Form.FormType.GRADUATION_CHECK,
                user_id=user
            )
        
        elif role == 'inspector':       # FOR INSPECTOR
            if not key_code:
                messages.error(request, 'Key code is required for inspectors')
                return render(request, 'complete_registration.html', 
                            {'error': 'Key code is required for inspectors'})       # FRONTEND
            # Validate key code
            if not validate_key_code(key_code):
                messages.error(request, 'Invalid key code')
                return render(request, 'complete_registration.html', 
                            {'error': 'Invalid key code'})                          # FRONTEND
            
            # Create new inspector user
            user = User.objects.create(
                email=verified_email,
                password=password,  
                name=name,
                student_code=student_code,
                role=User.Role.INSPECTOR
            )
        
        # Clean up session
        del request.session['verified_email']
        
        # Login user and redirect with trailing slash
        return redirect('/api/admin/')
        
    return render(request, 'complete_registration.html')

def validate_key_code(key_code):         # FOR INSPECTOR
    # check if key code exists in the list
    valid_key_codes = ['INSPECTOR123', 'INSPECTOR456']       # KEY CODES FOR INSPECTORS
    return key_code in valid_key_codes