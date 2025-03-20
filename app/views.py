from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, Teacher, Book, User
from functools import wraps

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'You are not logged in. Please log in to access the dashboard.')
            return redirect('login')
    return wrapper

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

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            try:
                user = User.objects.create_user(username=username, email=email, password=password, role=role)

                if role == 'student':
                    Student.objects.create(
                        user=user,
                        enrollment_number=request.POST.get('enrollment_number'),
                        department=request.POST.get('department'),
                        year=request.POST.get('year')
                    )
                elif role == 'teacher':
                    Teacher.objects.create(
                        user=user,
                        employee_id=request.POST.get('employee_id'),
                        subject=request.POST.get('subject')
                    )

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
        user = User.objects.get(email=email)

        if user.check_password(password):
            request.session['user_id'] = user.id
            messages.success(request, 'Login successful!')
            return redirect('dashboard_view')
        else:
            messages.error(request, 'Invalid email or password.')

    except User.DoesNotExist:
        messages.error(request, 'User with this email does not exist.')

    return render(request, 'login.html')

# forgot_password view :
def forgot_password_view(request):
    
    return render(request, 'forgot_password.html')

# profile_view :
@login_required
def profile_view(request):
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

    try:
        student = user.student_profile
    except Student.DoesNotExist:
        pass

    try:
        teacher = user.teacher_profile
    except Teacher.DoesNotExist:
        pass

    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)

        try:
            user.save()

            if student:
                student.enrollment_number = request.POST.get('enrollment_number', student.enrollment_number)
                student.department = request.POST.get('department', student.department)
                student.year = request.POST.get('year', student.year)
                student.save()

            elif teacher:
                teacher.employee_id = request.POST.get('employee_id', teacher.employee_id)
                teacher.subject = request.POST.get('subject', teacher.subject)
                teacher.save()

            messages.success(request, "Profile updated successfully!")
            return redirect('profile_view')

        except Exception as e:
            messages.error(request, f"Error updating profile: {str(e)}")

    return render(request, 'update_profile.html', {'user': user, 'student': student, 'teacher': teacher})

def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login_view')

@login_required
def delete_profile(request):
    user = request.user
    student = None
    teacher = None

    try:
        student = user.student_profile
    except Student.DoesNotExist:
        pass

    try:
        teacher = user.teacher_profile
    except Teacher.DoesNotExist:
        pass

    if request.method == "POST":
        if student:
            student.delete()
        elif teacher:
            teacher.delete()

        user.delete()

        messages.success(request, "Your profile has been deleted successfully.")
        return redirect('login_view')

    return render(request, 'delete_profile_confirmation.html', {'user': user})
