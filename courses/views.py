from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Module, CourseStudent
from .forms import CourseForm, ModuleForm, UserRegisterForm, NoAutoCompleteLoginForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse


def index(request):
    courses = Course.objects.all().order_by('-created_at')[:5]
    return render(request, 'index.html', {'courses': courses})


def course_list(request):
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'courses/course_list.html', {'courses': courses})

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            curso=form.save(commit=False)
            if request.user.is_authenticated and request.user.is_teacher(): #Verificamos que el usuario es profesor
                curso.teacher = request.user #Asignamos el actual usuario como profesor
                curso.save() 
                print("✅ Curso guardado")
                return redirect('courseteacher')
            else:
                print("⚠️ Usuario no autorizado para crear cursos")

        else:
            print("❌ Errores en el formulario:")
            print(form.errors)  # Esto mostrará qué campos están fallando
    else:
        form = CourseForm()
    return render(request, 'courses/add_course.html', {'form': form})


def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/edit_course.html', {'form': form, 'course': course})


def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'courses/delete_course.html', {'course': course})

def add_module(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            # Asignar el orden como último + 1
            last_order = Module.objects.filter(course=course).count()
            module.order = last_order + 1
            module.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = ModuleForm()
    
    return render(request, 'modules/add_module.html', {'form': form, 'course': course})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = Module.objects.filter(course=course)

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules
    })


def edit_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    course = module.course  # Accedes a su curso relacionado

    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = ModuleForm(instance=module)

    return render(request, 'modules/edit_module.html', {'form': form, 'course': course})




def delete_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    course = module.course
    if request.method == 'POST':
        course_id = course.id
        module.delete()
        return redirect('course_detail', course_id=course_id)
    return render(request, 'modules/delete_module.html', {'module': module})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu cuenta ha sido creada, puedes iniciar sesión')
            return redirect('login')
        print(form.errors)

    else:
        form = UserRegisterForm()
    
    return render(request, 'courses/register.html', {'form': form})

def agregarcourse(request, course_id):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_student():
            curso = get_object_or_404(Course, id=course_id)
            if not CourseStudent.objects.filter(student=request.user, course=curso).exists():
                queryset = CourseStudent.objects.filter(student=request.user)
                nuevo_order = queryset.count() + 1
                CourseStudent.objects.create(course=curso, student=request.user, order= nuevo_order)
                messages.success(request, 'Tu curso ha sido agregado')
        return redirect('coursestudent')

def coursestudent(request):
    if request.user.is_authenticated and request.user.is_student():
        cursos = CourseStudent.objects.filter(student=request.user).order_by('-id')
        return render(request, 'courses/coursestudent.html', {'cursos': cursos})
    return redirect ('course_list')

def courseteacher(request):
    if request.user.is_authenticated and request.user.is_teacher():
        cursos = Course.objects.filter(teacher=request.user).order_by('-id')
        print(f'Esto es lo que estamos enviando al template del profesor: {cursos}')
        return render(request, 'courses/courseteacher.html', {'cursos': cursos})
    return redirect ('course_list')


class CustomLoginView(LoginView):
    authentication_form = NoAutoCompleteLoginForm
    template_name = 'courses/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_teacher():
            return reverse('courseteacher')  # nombre de tu vista para profesores
        elif user.is_student():
            return reverse('coursestudent')   # nombre de tu vista para estudiantes
        return reverse('index')  # fallback opcional
