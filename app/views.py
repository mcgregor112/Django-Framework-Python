from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Student, Teacher, Book
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.decorators import login_required

def dashboard_view(request):
    
    student_count = Student.objects.count()
    teacher_count = Teacher.objects.count()
    book_count = Book.objects.count()  

    context = {
        'student_count': student_count,
        'teacher_count': teacher_count,
        'book_count': book_count,  
    }

    return render(request, 'dashboard.html', context)

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role', 'student')  
        is_active = request.POST.get('is_active', 'True') == 'True'
        is_staff = request.POST.get('is_staff', 'False') == 'True'

        User = get_user_model()

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('register_view')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register_view')

        try:
            user = User.objects.create_user(username=username, email=email, password=password, role=role, is_active=is_active, is_staff=is_staff)

            
            if role == 'student':
                enrollment_number = request.POST.get('enrollment_number')
                department = request.POST.get('department')
                year = request.POST.get('year')
                Student.objects.create(user=user, enrollment_number=enrollment_number, department=department, year=year)
            elif role == 'teacher':
                employee_id = request.POST.get('employee_id')
                subject = request.POST.get('subject')
                Teacher.objects.create(user=user, employee_id=employee_id, subject=subject)

            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login_view')
        except Exception as e:
            messages.error(request, f'Error during registration: {e}')
            return redirect('register_view')

    return render(request, 'register.html')


def login_view(request):
    email = None
    password = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
    try:
        
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard_view')
        else:
            messages.error(request, 'Invalid email or password.')

    except MultipleObjectsReturned:
            messages.error(request, 'Multiple accounts found with this email. Contact support.')        

    return render(request, 'login.html')

# Logout View
# def logout_view(request):
#     if request.user.is_authenticated:
#         logout(request)
#         messages.success(request, 'You have been logged out.')
#     return redirect('login_view')

# Forgot Password View
def forgot_password_view(request):
    
    return render(request, 'forgot_password.html')

@login_required
def profile_view(request):
    """View to display the profile details."""
    user = request.user
    student = None
    teacher = None

    
    if hasattr(user, 'student_profile'):  
        student = user.student_profile
    elif hasattr(user, 'teacher_profile'):  
        teacher = user.teacher_profile

    context = {
        'user': user,
        'student': student,
        'teacher': teacher,
    }

    return render(request, 'profile.html', context)

@login_required
def update_profile(request):
    user = request.user
    student = None
    teacher = None

    if hasattr(user, 'student_profile'):  
        student = user.student_profile
    elif hasattr(user, 'teacher_profile'):  
        teacher = user.teacher_profile

    if request.method == "POST":
        
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        if student:
            student.enrollment_number = request.POST.get('enrollment_number')
            student.department = request.POST.get('department')
            student.year = request.POST.get('year')
            student.save()

       
        elif teacher:
            teacher.employee_id = request.POST.get('employee_id')
            teacher.subject = request.POST.get('subject')
            teacher.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile_view')

    context = {
        'user': user,
        'student': student,
        'teacher': teacher,
    }
    return render(request, 'update_profile.html', context)

def logout_view(request):
    """Logout the user and redirect to the home page."""
    logout(request)
    return redirect('login_view')


@login_required
def delete_profile(request):
    user = request.user
    student = None
    teacher = None

    
    if hasattr(user, 'student_profile'):  
        student = user.student_profile
    elif hasattr(user, 'teacher_profile'):  
        teacher = user.teacher_profile

    if request.method == "POST":
        
        if student:
            student.delete()
        elif teacher:
            teacher.delete()

        user.delete()

        messages.success(request, "Your profile has been deleted successfully.")
        return redirect('login_view') 

    return render(request, 'delete_profile_confirmation.html', {'user': user})

def library_view(request):
    books = Book.objects.all()  
    return render(request, 'library.html', {'books': books})

def student_view(request):
    student = Student.objects.all()
    return render(request, 'student.html', {'student' : student})