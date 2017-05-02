from django import forms

from .models import Course, Module, Component

class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('code','name', 'description', 'allow_enroll', 'instructor', 'category')
        widgets = {'instructor': forms.HiddenInput()}
        exclude = [ 'instructor' ]

class ModuleForm(forms.ModelForm):

    class Meta:
        model = Module
        fields = ('course','name', 'visible','instructor')
        widgets = {'course': forms.HiddenInput(),
        			'instructor': forms.HiddenInput()}

class TextForm(forms.ModelForm):

    class Meta:
        model = Component
        fields = ('module','name', 'instructor' , 'component_type' , 'text')
        widgets = {'module': forms.HiddenInput(),
                    'instructor': forms.HiddenInput(),
                    'component_type': forms.HiddenInput()}

class ImageForm(forms.ModelForm):

    class Meta:
        model = Component
        fields = ('module','name', 'instructor' , 'component_type' , 'image')
        widgets = {'module': forms.HiddenInput(),
            'instructor': forms.HiddenInput(),
            'component_type': forms.HiddenInput()}

class VideoForm(forms.ModelForm):

    class Meta:
        model = Component
        fields = ('module','name', 'instructor' , 'component_type' , 'video')
        widgets = {'module': forms.HiddenInput(),
            'instructor': forms.HiddenInput(),
            'component_type': forms.HiddenInput()}

class FileForm(forms.ModelForm):

    class Meta:
        model = Component
        fields = ('module','name', 'instructor' , 'component_type' , 'file')
        widgets = {'module': forms.HiddenInput(),
                    'instructor': forms.HiddenInput(),
                    'component_type': forms.HiddenInput()}