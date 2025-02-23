from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.contrib.sessions.middleware import SessionMiddleware
from main.models import OTPVerification, User, Form
from main.forms import EmailForm, OTPVerificationForm
from django.utils import timezone
from datetime import timedelta

class SignupTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup_with_otp')
        self.verify_url = reverse('verify_otp')
        self.complete_url = reverse('complete_registration')
        
    def test_signup_get(self):
        """Test GET request to signup page"""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup_with_otp.html')
        self.assertIsInstance(response.context['form'], EmailForm)

    def test_signup_post_valid_email(self):
        """Test successful OTP generation and email sending"""
        data = {'email': 'test@example.com'}
        response = self.client.post(self.signup_url, data)
        self.assertRedirects(response, self.verify_url)
        
        otp_obj = OTPVerification.objects.filter(email='test@example.com').first()
        self.assertIsNotNone(otp_obj)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], 'test@example.com')

    def test_verify_otp_without_email(self):
        """Test accessing verify page without email in session"""
        response = self.client.get(self.verify_url)
        self.assertRedirects(response, self.signup_url)

    def test_verify_otp_valid(self):
        """Test successful OTP verification"""
        email = 'test@example.com'
        otp = '123456'
        OTPVerification.objects.create(
            email=email,
            otp=otp,
            reference_otp='REF123'
        )
        
        session = self.client.session
        session['email_for_otp'] = email
        session.save()
        
        response = self.client.post(self.verify_url, {'otp': otp})
        self.assertRedirects(response, self.complete_url)

    def test_verify_otp_invalid(self):
        """Test invalid OTP verification"""
        email = 'test@example.com'
        session = self.client.session
        session['email_for_otp'] = email
        session.save()
        
        # Use an incorrect OTP of exactly 6 characters
        response = self.client.post(self.verify_url, {'otp': '000000'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid or expired OTP', response.content.decode())

        # Use an incorrect OTP that is too long (should trigger form validation)
        response = self.client.post(self.verify_url, {'otp': '1234567'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('OTP must be exactly 6 digits', response.content.decode())

        # Use an incorrect OTP that is too short
        response = self.client.post(self.verify_url, {'otp': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('OTP must be exactly 6 digits', response.content.decode())

    def test_complete_registration_student(self):
        """Test successful student registration"""
        session = self.client.session
        session['verified_email'] = 'test@example.com'
        session.save()
        
        data = {
            'name': 'Test Student',
            'password': 'testpass123',
            'confirm-password': 'testpass123',
            'role': 'student',
            'student-code': 'STU123'
        }
        
        response = self.client.post(self.complete_url, data, follow=True)
        self.assertRedirects(response, '/api/admin/', status_code=302, target_status_code=200)
        
        user = User.objects.filter(email='test@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.role, User.Role.STUDENT)
        self.assertEqual(user.student_code, 'STU123')
        
        form = Form.objects.filter(user_id=user).first()
        self.assertIsNotNone(form)
        self.assertEqual(form.form_type, Form.FormType.GRADUATION_CHECK)

    def test_complete_registration_inspector(self):
        """Test successful inspector registration"""
        session = self.client.session
        session['verified_email'] = 'inspector@example.com'
        session.save()
        
        data = {
            'name': 'Test Inspector',
            'password': 'testpass123',
            'confirm-password': 'testpass123',
            'role': 'inspector',
            'key-code': 'INSPECTOR123'
        }
        
        response = self.client.post(self.complete_url, data, follow=True)
        self.assertRedirects(response, '/api/admin/', status_code=302, target_status_code=200)
        
        user = User.objects.filter(email='inspector@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.role, User.Role.INSPECTOR)

    def test_complete_registration_password_mismatch(self):
        """Test registration with mismatched passwords"""
        session = self.client.session
        session['verified_email'] = 'test@example.com'
        session.save()
        
        data = {
            'name': 'Test Student',
            'password': 'testpass123',
            'confirm-password': 'different',
            'role': 'student',
            'student-code': 'STU123'
        }
        
        response = self.client.post(self.complete_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Passwords do not match', response.content.decode())

    def test_complete_registration_invalid_key_code(self):
        """Test inspector registration with invalid key code"""
        session = self.client.session
        session['verified_email'] = 'inspector@example.com'
        session.save()
        
        data = {
            'name': 'Test Inspector',
            'password': 'testpass123',
            'confirm-password': 'testpass123',
            'role': 'inspector',
            'key-code': 'INVALID'
        }
        
        response = self.client.post(self.complete_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid key code', response.content.decode())