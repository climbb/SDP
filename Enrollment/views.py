from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CourseForm, ModuleForm, TextForm, ImageForm, VideoForm, FileForm
from .models import Participant, Course, Enrollment, Module, Component, Instructor, Category
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django import forms

import datetime
from django.contrib.auth.decorators import login_required


#@login_required
#def view(request):
	# courses_1 = Course.objects.filter(category='MERQ').order_by('enrollmentNo')
	# courses_2 = Course.objects.filter(category='MRKT').order_by('enrollmentNo')
	# courses_3 = Course.objects.filter(category='RKMN').order_by('enrollmentNo')
	# courses_4 = Course.objects.filter(category='SCRT').order_by('enrollmentNo')
	# courses_5 = Course.objects.filter(category='FIMO').order_by('enrollmentNo')
	# courses_6 = Course.objects.filter(category='OPER').order_by('enrollmentNo')
	# courses_7 = Course.objects.filter(category='IFTC').order_by('enrollmentNo')

 #    return render(request, 'enrollment/index.html', {'courses_1': courses_1, 'courses_2': courses_2, 'courses_3': courses_3, 'courses_4': courses_4, 'courses_5': courses_5, 'courses_6': courses_6, 'courses_7': courses_7})

@login_required
def index(request):

	courses_list = []

	for category in Category.objects.all():
		courses_list.append(Course.objects.filter(category=category).order_by('enrollmentNo'))


	categories = Category.objects.all()

	return render(request, 'enrollment/index.html', {'courses_list': courses_list, 'categories': categories})

@login_required
def enroll(request):

	courses_list = []

	for category in Category.objects.all():
		courses_list.append(Course.objects.filter(category=category, allow_enroll=True).order_by('enrollmentNo'))

	
	categories = Category.objects.all()

	return render(request, 'enrollment/enroll.html', {'courses_list': courses_list, 'categories': categories})

@login_required
def course_detail(request, pk):
	course = get_object_or_404(Course, pk=pk)
	mode = 0
	# mode: 0 = for course list view
	# 		1 = for enrollment view
	return render(request, 'enrollment/course_detail.html', {'mode': mode, 'course': course})

@login_required
def enroll_course_detail(request, pk):
	course = get_object_or_404(Course, pk=pk)
	mode = 1
	# mode: 0 = for course list view
	# 		1 = for enrollment view
	return render(request, 'enrollment/course_detail.html', {'mode': mode, 'course': course})


@login_required
def view_users(request):
	users = Participant.objects.all()
	return render(request, 'enrollment/view_users.html', {'users': users})

@login_required
def view_user_completed(request, pk):
	user = get_object_or_404(User, pk=pk)
	participant = get_object_or_404(Participant, user=user)
	enrollments = Enrollment.objects.filter(participant=user, state='FI').order_by('date_finish')
	return render(request, 'enrollment/view_user_completed.html', {'enrollments': enrollments, 'user': user, 'participant': participant})

@login_required
def course_new(request):
	if request.method == "POST":
		form = CourseForm(request.POST)
		if form.is_valid():
			course = form.save(commit=False)
			course.instructor = request.user
			course.save()
			return redirect('/managecourses')
	else:
		form = CourseForm()
	return render(request, 'enrollment/createnewcourse.html', {'form': form})

@login_required
def add(request,pk):
	course = get_object_or_404(Course, pk=pk)
	if not Enrollment.objects.filter(participant=request.user, state='PR'):
		new_enrollment = Enrollment.objects.create(course=course, participant=request.user, date_enrollment=datetime.date.today(), state='PR')
		course.enrollmentNo += 1;
		return render(request, 'enrollment/enroll_success.html', {'course': course})
	else:
		return render(request, 'enrollment/enroll_fail.html', {'course': course})


@login_required
def mycourses(request):
	enrollments = Enrollment.objects.filter(participant=request.user).order_by('-state', 'course')
	return render(request, 'enrollment/mycourses.html',{'enrollments': enrollments})

@login_required
def managecourses(request):
	if request.user.groups.filter(name='Instructor').exists(): #Instructor.objects.filter(user=request.user).exists():
		courses = Course.objects.filter(instructor=request.user).order_by('name')
		return render(request, 'enrollment/managecourses.html', {'courses': courses})
	else:
		return redirect('/')

@login_required
def course_modules(request, pk):
	enrollment = get_object_or_404(Enrollment, pk=pk)
	course = get_object_or_404(Course, pk=enrollment.course.id)
	modules = Module.objects.filter(course=course, visible=True, position__lte=enrollment.progress).order_by('position')
	totalModules = Module.objects.filter(course=course, visible=True).count()
	if enrollment.progress > totalModules:
		enrollment.progress = totalModules
		enrollment.save()
	if Enrollment.objects.filter(course=course, participant=request.user).exists():
		return render(request, 'enrollment/course_modules.html', {'totalModules': totalModules, 'enrollment': enrollment, 'course': course, 'modules': modules})
	else:
		return redirect('/')

@login_required
def course_drop(request, pk):
	enrollment = get_object_or_404(Enrollment, pk=pk)
	enrollment.delete()
	return redirect('/mycourses')

@login_required
def course_module_detail(request, pk1, pk2):
	enrollment = get_object_or_404(Enrollment, pk=pk1)
	course = get_object_or_404(Course, pk=enrollment.course.id)
	module = get_object_or_404(Module, pk=pk2)
	components = module.getComponents
	totalModules = Module.objects.filter(course=course, visible=True).count()
	if (enrollment.progress == module.position):
		enrollment.progress += 1
		if(enrollment.progress == totalModules):
			enrollment.state = 'FI'
			enrollment.date_finish = datetime.date.today()
		enrollment.save()
	if Enrollment.objects.filter(course=course, participant=request.user).exists():
		return render(request, 'enrollment/course_module_detail.html', {'enrollment': enrollment, 'course': course, 'module': module, 'components': components})
	else:
		return redirect('/')

@login_required
def course_component_detail(request, pk1, pk2, pk3):
	mode = 0
	# mode: 0 = for participant view
	# 		1 = for instructor edit view
	enrollment = get_object_or_404(Enrollment, pk=pk1)
	course = get_object_or_404(Course, pk=enrollment.course.id)
	module = get_object_or_404(Module, pk=pk2)
	component = get_object_or_404(Component, pk=pk3)
	if (Enrollment.objects.filter(course=course, participant=request.user).exists() or Course.objects.filter(id=course.id, instructor=request.user).exists()):
		return render(request, 'enrollment/course_component_detail.html', {'mode': mode, 'course': course, 'module': module, 'component': component})
	else:
		return redirect('/')

@login_required
def course_component_detail_instructor(request, pk1, pk2, pk3):
	mode = 1
	# mode: 0 = for participant view
	# 		1 = for instructor edit view
	course = get_object_or_404(Course, pk=pk1)
	module = get_object_or_404(Module, pk=pk2)
	component = get_object_or_404(Component, pk=pk3)
	if (course.instructor == request.user):
		return render(request, 'enrollment/course_component_detail.html', {'mode': mode, 'course': course, 'module': module, 'component': component})
	else:
		return redirect('/')		

@login_required
def complete_module(request, pk1, pk2):
	enrollment = get_object_or_404(Enrollment, pk=pk1)
	course = get_object_or_404(Course, pk=enrollment.course.id)
	module = get_object_or_404(Module, pk=pk2)
	totalModules = Module.objects.filter(course=course, visible=True).count()
	if (enrollment.progress == module.position):
		enrollment.progress += 1
		if(enrollment.progress == totalModules):
			enrollment.state = 'FI'
			enrollment.date_finish = datetime.date.today()
		enrollment.save()
		return redirect('../')
	else:
		return redirect('/')

@login_required
def edit_course(request, pk):
	course = get_object_or_404(Course, pk=pk)
	modules = course.getModules
	# modules = Module.objects.filter(course=course)
	return render(request, 'enrollment/edit_course.html', {'course': course, 'modules': modules})

@login_required
def edit_course_preferences(request, pk):
	course = get_object_or_404(Course, pk=pk)
	if request.method == "POST":
		form = CourseForm(request.POST,instance=course)
		if form.is_valid():
			course = form.save(commit=False)
			course.save()
			return redirect('../')
	else:
		form = CourseForm(initial= {'code': course.code,'name': course.name,'description': course.description, 'allow_enroll': course.allow_enroll, 'instructor': request.user, 'category': course.category},instance=course)
		return render(request, 'enrollment/edit_course_preferences.html', {'form': form, 'course': course})

@login_required
def module_new(request, pk1):
	if request.method == "POST":
		form = ModuleForm(request.POST)
		if form.is_valid():
			module = form.save(commit=False)
			module.position = Module.objects.filter(course=module.course).count() 
			module.save()
			return redirect('../')
	else:
		course = get_object_or_404(Course, pk=pk1)
		form = ModuleForm(initial= {'course': course, 'instructor': request.user})
		return render(request, 'enrollment/add_new_module.html', {'form': form, 'course': course})

@login_required
def module_delete(request, pk1, pk2):
	course = get_object_or_404(Course, pk=pk1)
	module = get_object_or_404(Module, pk=pk2)
	module.delete()
	modules = Module.objects.filter(course=course)
	return render(request, 'enrollment/edit_course.html', { 'course': course, 'modules': modules})

@login_required
def module_components(request, pk1, pk2):
	course = get_object_or_404(Course, pk=pk1)
	module = get_object_or_404(Module, pk=pk2)
	components = module.getComponents
	if (request.user.groups.filter(name='Instructor').exists()) and (course.instructor == request.user):
		return render(request, 'enrollment/edit_components.html', {'course': course, 'module': module, 'components': components})
	else:
		return redirect('/')

@login_required
def moveup_module(request, pk1, pk2):
	print ("moving up a module")
	course = get_object_or_404(Course, pk=pk1)
	module = get_object_or_404(Module, pk=pk2)
	totalModules = Module.objects.filter(course=course, visible=True).count()
	module.position = module.position - 1
	if module.position == -1 or module.position == totalModules: 
		print ("module will not move because it's on the top or the bottom")
		return redirect('../../../')
	module.save()
	return redirect('../../../')

@login_required
def movedown_module(request, pk1, pk2):
	print ("moving down a module")
	course = get_object_or_404(Course, pk=pk1)
	module = get_object_or_404(Module, pk=pk2)
	totalModules = Module.objects.filter(course=course, visible=True).count()
	module.position = module.position + 1
	if module.position == -1 or module.position == totalModules: 
		print ("module will not move because it's on the top or the bottom")
		return redirect('../../../')
	module.save()
	return redirect('../../../')


@login_required
def component_add_text(request, pk1, pk2):
	if request.method == "POST":
		form = TextForm(request.POST)
		if form.is_valid():
			component = form.save(commit=False)
			component.position = Component.objects.filter(module=component.module).count()
			component.save()
			return redirect('../')
	else:
		course = get_object_or_404(Course, pk=pk1)
		module = get_object_or_404(Module, pk=pk2)
		if (request.user.groups.filter(name='Instructor').exists()) and (course.instructor == request.user):
			form = TextForm(initial= {'module': module, 'instructor': request.user, 'component_type': 'TXT'})
			return render(request, 'enrollment/component_add_text.html', {'form': form,'course': course, 'module': module})
		else:
			return redirect('/')

@login_required
def component_add_image(request, pk1, pk2):
	if request.method == "POST":
		form = ImageForm(request.POST, request.FILES)
		if form.is_valid():
			component = form.save(commit=False)
			component.position = Component.objects.filter(module=component.module).count()
			component.save()
			return redirect('../')
	else:
		course = get_object_or_404(Course, pk=pk1)
		module = get_object_or_404(Module, pk=pk2)
		if (request.user.groups.filter(name='Instructor').exists()) and (course.instructor == request.user):
			form = ImageForm(initial= {'module': module, 'instructor': request.user, 'component_type': 'IMG'})
			return render(request, 'enrollment/component_add_image.html', {'form': form,'course': course, 'module': module})
		else:
			return redirect('/')

@login_required
def component_add_video(request, pk1, pk2):
	if request.method == "POST":
		form = VideoForm(request.POST, request.FILES)
		if form.is_valid():
			component = form.save(commit=False)
			component.position = Component.objects.filter(module=component.module).count()
			component.save()
			return redirect('../')
	else:
		course = get_object_or_404(Course, pk=pk1)
		module = get_object_or_404(Module, pk=pk2)
		if (request.user.groups.filter(name='Instructor').exists()) and (course.instructor == request.user):
			form = VideoForm(initial= {'module': module, 'instructor': request.user, 'component_type': 'VID'})
			return render(request, 'enrollment/component_add_video.html', {'form': form,'course': course, 'module': module})
		else:
			return redirect('/')

@login_required
def component_add_file(request, pk1, pk2):
	if request.method == "POST":
		form = FileForm(request.POST, request.FILES)
		if form.is_valid():
			component = form.save(commit=False)
			component.position = Component.objects.filter(module=component.module).count()
			component.save()
			return redirect('../')
	else:
		course = get_object_or_404(Course, pk=pk1)
		module = get_object_or_404(Module, pk=pk2)
		if (request.user.groups.filter(name='Instructor').exists()) and (course.instructor == request.user):
			form = FileForm(initial= {'module': module, 'instructor': request.user, 'component_type': 'FIL'})
			return render(request, 'enrollment/component_add_file.html', {'form': form,'course': course, 'module': module})
		else:
			return redirect('/')

@login_required
def delete_component(request, pk1, pk2, pk3):
	course = get_object_or_404(Course, pk=pk1)
	module = get_object_or_404(Module, pk=pk2)
	component = get_object_or_404(Component, pk=pk3)
	component.delete()
	modules = Module.objects.filter(course=course)
	return redirect('../../../')
	#return render(request, 'enrollment/edit_course.html', { 'course': course, 'modules': modules})

@login_required
def edit_module(request, pk1, pk2):
	course = get_object_or_404(Course, pk=pk1)
	module = get_object_or_404(Module, pk=pk2)
	if request.method == "POST":
		form = ModuleForm(request.POST,instance=module)
		if form.is_valid():
			module = form.save(commit=False)
			module.save()
			return redirect('/managecourses')
	else:
		form = ModuleForm(initial= {'course': course,'name': module.name,'visible': module.visible, 'instructor': request.user},instance=module)
		return render(request, 'enrollment/edit_module.html', {'form': form, 'course': course, 'module': module})

@login_required
def component_edit_text(request, pk1, pk2, pk3):
	course = get_object_or_404(Course, pk=pk1)
	module = get_object_or_404(Module, pk=pk2)
	component = get_object_or_404(Component, pk=pk3)
	if request.method == "POST":
		form = TextForm(request.POST,instance=component)
		if form.is_valid():
			component = form.save(commit=False)
			component.save()
			return redirect('/managecourses')
	else:
		if (request.user.groups.filter(name='Instructor').exists()) and (course.instructor == request.user):
			form = TextForm(initial= {'module': module, 'instructor': request.user, 'component_type': 'TXT'},instance=component)
			return render(request, 'enrollment/component_edit_text.html', {'form': form,'course': course, 'module': module, 'component': component})
		else:
			return redirect('/')

@login_required
def component_edit_image(request, pk1, pk2, pk3):
	course = get_object_or_404(Course, pk=pk1)
	module = get_object_or_404(Module, pk=pk2)
	component = get_object_or_404(Component, pk=pk3)
	if request.method == "POST":
		form = ImageForm(request.POST, request.FILES,instance=component)
		if form.is_valid():
			component = form.save(commit=False)
			component.save()
			return redirect('/managecourses')
	else:
		if (request.user.groups.filter(name='Instructor').exists()) and (course.instructor == request.user):
			form = ImageForm(initial= {'module': module, 'instructor': request.user, 'component_type': 'IMG'},instance=component)
			return render(request, 'enrollment/component_edit_image.html', {'form': form,'course': course, 'module': module,'component': component})
		else:
			return redirect('/')

@login_required
def component_edit_video(request, pk1, pk2, pk3):
	course = get_object_or_404(Course, pk=pk1)
	module = get_object_or_404(Module, pk=pk2)
	component = get_object_or_404(Component, pk=pk3)
	if request.method == "POST":
		form = VideoForm(request.POST, request.FILES,instance=component)
		if form.is_valid():
			component = form.save(commit=False)
			component.save()
			return redirect('/managecourses')
	else:
		if (request.user.groups.filter(name='Instructor').exists()) and (course.instructor == request.user):
			form = VideoForm(initial= {'module': module, 'instructor': request.user, 'component_type': 'VID'},instance=component)
			return render(request, 'enrollment/component_edit_video.html', {'form': form,'course': course, 'module': module, 'component': component})
		else:
			return redirect('/')

@login_required
def component_edit_file(request, pk1, pk2, pk3):
	course = get_object_or_404(Course, pk=pk1)
	module = get_object_or_404(Module, pk=pk2)
	component = get_object_or_404(Component, pk=pk3)
	if request.method == "POST":
		form = FileForm(request.POST, request.FILES,instance=component)
		if form.is_valid():
			component = form.save(commit=False)
			component.save()
			return redirect('/managecourses')
	else:
		if (request.user.groups.filter(name='Instructor').exists()) and (course.instructor == request.user):
			form = FileForm(initial= {'module': module, 'instructor': request.user, 'component_type': 'FIL'},instance=component)
			return render(request, 'enrollment/component_edit_file.html', {'form': form,'course': course, 'module': module,'component': component})
		else:
			return redirect('/')

@login_required
def moveup_component(request, pk1, pk2, pk3):
	print ("moving up a component")
	course = get_object_or_404(Course, pk=pk1)
	module = get_object_or_404(Module, pk=pk2)
	component = get_object_or_404(Component, pk=pk3)
	component.position = component.position - 1
	if component.position == -1 or component.position == Component.objects.filter(module=pk2).count()+1: 
		print ("component will not move because it's on the top or the bottom")
		return redirect('../../../')
	component.save()
	modules = Module.objects.filter(course=course)
	return redirect('../../../')

@login_required
def movedown_component(request, pk1, pk2, pk3):
	print ("moving down a component")
	course = get_object_or_404(Course, pk=pk1)
	module = get_object_or_404(Module, pk=pk2)
	component = get_object_or_404(Component, pk=pk3)
	component.position = component.position + 1
	if component.position == -1 or component.position == Component.objects.filter(module=pk2).count()+1: 
		print ("component will not move because it's on the top or the bottom")
		return redirect('../../../')
	component.save()
	modules = Module.objects.filter(course=course)
	return redirect('../../../')

