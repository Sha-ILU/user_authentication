from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import User


@csrf_exempt
@require_POST
def register(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')

    if not all([first_name, last_name, email, username, password]):
        return JsonResponse({'error': 'All fields are required.'}, status=400)

    try:
        User.objects.get(username=username)
        return JsonResponse({'error': 'Username already exists.'}, status=400)
    except ObjectDoesNotExist:
        pass

    try:
        User.objects.get(email=email)
        return JsonResponse({'error': 'Email already exists.'}, status=400)
    except ObjectDoesNotExist:
        pass

    user = User.objects.create_user(username=username, email=email, password=password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    return JsonResponse({'success': 'User registered successfully.'})

@csrf_exempt
@require_POST
def verify(request):
    email_or_username = request.POST.get('email_or_username')
    otp = request.POST.get('otp')

    if not all([email_or_username, otp]):
        return JsonResponse({'error': 'Email/Username and OTP are required.'}, status=400)

    user = User.objects.filter(email=email_or_username).first() or User.objects.filter(username=email_or_username).first()

    if not user:
        return JsonResponse({'error': 'User not found.'}, status=404)

    if user.otp != otp:
        return JsonResponse({'error': 'Invalid OTP.'}, status=400)

    user.is_verified = True
    user.save()

    return JsonResponse({'success': 'User verified successfully.'})

@csrf_exempt
@require_POST
def login(request):
    email_or_username = request.POST.get('email_or_username')
    otp = request.POST.get('otp')

    if not all([email_or_username, otp]):
        return JsonResponse({'error': 'Email/Username and OTP are required.'}, status=400)

    user = authenticate(request, username=email_or_username, password=otp)

    if user is None:
        return JsonResponse({'error': 'Invalid credentials.'}, status=400)

    if not user.is_verified:
        return JsonResponse({'error': 'User is not verified.'}, status=400)

    login(request, user)

    # Generate refresh token and access token (You will need to implement this logic)

    return JsonResponse({'success': 'User logged in successfully.'})

@csrf_exempt
@require_POST
def forgot_password(request):
    email_or_username = request.POST.get('email_or_username')

    if not email_or_username:
        return JsonResponse({'error': 'Email/Username is required.'}, status=400)

    user = User.objects.filter(email=email_or_username).first() or User.objects.filter(username=email_or_username).first()

    if not user:
        return JsonResponse({'error': 'User not found.'}, status=404)

    # Generate OTP and send it to the user's email (You will need to implement this logic)

    return JsonResponse({'success': 'OTP sent successfully.'})

@csrf_exempt
@require_POST
def reset_password(request):
    email_or_username = request.POST.get('email_or_username')
    otp = request.POST.get('otp')

    if not all([email_or_username, otp]):
        return JsonResponse({'error': 'Email/Username and OTP are required.'}, status=400)

    user = User.objects.filter(email=email_or_username).first() or User.objects.filter(username=email_or_username).first()

    if not user:
        return JsonResponse({'error': 'User not found.'}, status=404)

    if user.otp != otp:
        return JsonResponse({'error': 'Invalid OTP.'}, status=400)

    

    return JsonResponse({'success': 'Password reset successfully.'})
