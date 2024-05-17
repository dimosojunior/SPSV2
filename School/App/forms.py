from django import forms
from .models import *

from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm, UserChangeForm
from django.contrib.auth import authenticate

from django.conf import settings










class StudentsSearchForm(forms.ModelForm):
	
	StudentName = forms.CharField(
		required=False,
	#label=False,
		widget=forms.TextInput(attrs={'id' :'StudentName', 'placeholder' : 'Enter Student Name'})

	)
	export_to_CSV = forms.BooleanField(required=False)
	#start_date = forms.DateTimeField(required=False)
	#end_date = forms.DateTimeField(required=False)


	class Meta:
		model = Students
		fields =['Class', 'StudentName', 'export_to_CSV']



class ReceiveStudentFeeeForm(forms.ModelForm):
	# is_received = forms.BooleanField(
	# 	required=True,
	# #label=False,
		

	# )
	ReceivedAmount = forms.IntegerField(
		required=True,
	)
	
	

	class Meta:
		model = Students
		fields =['ReceivedAmount','Semister']





class StudentCreateForm(forms.ModelForm):
	StudentName = forms.CharField(
		required=True,
	#label=False,
		
	)

	ParentNumber = forms.CharField(
		required=True,
	#label=False,
		
	)

	StudentLocation = forms.CharField(
		required=True,
	#label=False,
		
	)

	Gender = forms.CharField(
		required=True,
	#label=False,
		
	)
	


	class Meta:
		model = Students
		fields =[
			
			'Class', 
			'Year', 
			'StudentName', 
			'ParentNumber', 
			'StudentImage',
			'Gender',
			'StudentLocation'

			
			#'time_stamp',
			#'last_updated'


			]

	def clean_Class(self):
		Class = self.cleaned_data.get('Class')
		if not Class:
			raise forms.ValidationError('Please enter Student class')
		#for instance in Stock.objects.all():
			#if instance.category == category:
				#raise forms.ValidationError(category + 'is already created')

		return Class
	def clean_StudentName(self):
		StudentName = self.cleaned_data.get('StudentName')
		if not StudentName:
			raise forms.ValidationError('Please enter Student Name')
		#for instance in Stock.objects.all():
			#if instance.item_name == item_name:
				#raise forms.ValidationError(item_name + ' is already created')
		return StudentName




class AddNewClassForm(forms.ModelForm):
	ClassName = forms.CharField(
		required=True,
	#label=False,
		
	)

	Level = forms.CharField(
		required=True,
	#label=False,
		
	)

	ClassFee = forms.IntegerField(
		required=True,
	#label=False,
		
	)

	SemisterFee = forms.IntegerField(
		required=True,
	#label=False,
		
	)
	


	class Meta:
		model = Classes
		fields =[
			
			'ClassName', 
			'ClassFee', 
			'SemisterFee', 
			'Level'
			

			
			#'time_stamp',
			#'last_updated'


			]

class AddNewYearForm(forms.ModelForm):
	Year = forms.CharField(
		required=True,
	#label=False,
		
	)
	


	class Meta:
		model = Years
		fields =[
			
			'Year' 
			
			

			
			#'time_stamp',
			#'last_updated'


			]