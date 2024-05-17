from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from .models import *
from .forms import *
from django.http import HttpResponse
from datetime import datetime, timedelta
import pyotp
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
import os
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator


from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#C:\Users\DIMOSO JR\Desktop\ProjectWork\SmartInvigilation\SmartInvigilationProject\SmartInvigilationApp
print(BASE_DIR)
from django.core.files.base import ContentFile

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from .resources import *
from tablib import Dataset

import datetime

import csv

#@login_required(login_url='login')
def home(request):
    

    return render(request,'App/home.html')









#@login_required(login_url='login')
def AllClasses(request):
    classes = Classes.objects.filter(
            Level__icontains="Primary Level"
        )

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(classes,6)
    page = request.GET.get('page')
    try:
        classes=paginator.page(page)
    except PageNotAnInteger:
        classes=paginator.page(1)
    except EmptyPage:
        classes=paginator.page(paginator.num_pages)



    context = {
        "classes":classes,
        "page":page,
    }

    return render(request,'App/AllClasses.html',context)





def AllClasses_O_Level(request):
    classes = Classes.objects.filter(
            Level__icontains="O-Level"
        )

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(classes,6)
    page = request.GET.get('page')
    try:
        classes=paginator.page(page)
    except PageNotAnInteger:
        classes=paginator.page(1)
    except EmptyPage:
        classes=paginator.page(paginator.num_pages)



    context = {
        "classes":classes,
        "page":page,
    }

    return render(request,'App/AllClasses_O_Level.html',context)


@login_required(login_url='login')
def AllYearsPage(request, id):
    
    classId = Classes.objects.get(id=id)
    classId_id = classId.id
    classId_name = classId.ClassName
    # print(f"IDDDDD {classId.id}")
    request.session['classId_id'] = classId_id
    request.session['classId_name'] = classId_name

    queryset = Years.objects.all()

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,6)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset":queryset,
        "page":page,
    }

    return render(request,'App/AllYearsPage.html',context)


@login_required(login_url='login')
def AllStudents(request, id):
    classId_id = request.session.get('classId_id', '')
    classId_name = request.session.get('classId_name', '')


    # classId = Classes.objects.get(id=id)
    className = classId_name

    yearId = Years.objects.get(id=id)
    yearName = yearId.Year

    print(f"Class ID {classId_id}")
    # print(f"Year ID {yearId.id}")

    form = StudentsSearchForm(request.POST or None)
    # x= datetime.now()
    # current_date = x.strftime('%d-%m-%Y %H:%M')
    

    queryset = Students.objects.filter(

            Class__id__icontains = classId_id,
            Year__id__icontains = yearId.id,

        ).order_by('id')


    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,10)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)
    
    form = StudentsSearchForm(request.POST or None)




    #MWISHO HAP




    context ={
        "queryset":queryset,
        "form":form,
        "page":page,
        # "current_date":current_date,
        "className":className,
    }

    #kwa ajili ya kufilter items and category ktk form
    if request.method == 'POST':
        #category__icontains=form['category'].value(),
        Class = form['Class'].value()

        

                                        
        queryset = Students.objects.filter(
                                        StudentName__icontains=form['StudentName'].value(),
                                        Class__id__icontains = classId_id,
                                        Year__id__icontains = yearId.id,

                                        #last_updated__gte=form['start_date'].value(),
                                        # last_updated__lte=form['end_date'].value()
                                        #last_updated__range=[
                                            #form['start_date'].value(),
                                            #form['end_date'].value()
                                        #]
            )
        if (Class != ''):
            queryset = Students.objects.filter(
                    Year__id__icontains = yearId.id,
                )
            queryset = queryset.filter(Class_id=Class)

            #To SET  PAGINATION IN STOCK LIST PAGE
            paginator = Paginator(queryset,10)
            page = request.GET.get('page')
            try:
                queryset=paginator.page(page)
            except PageNotAnInteger:
                queryset=paginator.page(1)
            except EmptyPage:
                queryset=paginator.page(paginator.num_pages)
            #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI
        
        #hii ni kwa ajili ya kudownload ile page nzima ya stock endapo mtu akiweka tiki kwenye field export to csv
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['content-Disposition'] = 'attachment; filename="Students Details.csv"'
            writer = csv.writer(response)
            writer.writerow(['Student Name','Class', 'Year', 'Parent Number','Location', 'Total Amount Paid', 'Total Amount Paid Semister 1', 'Total Amount Paid Semister 2', 'Total Amount Paid Semister 3', 'Total Amount Remained', 'Amount Remained Semister 1', 'Amount Remained Semister 2', 'Amount Remained Semister 3'])
            instance = queryset
            for student in queryset:
                writer.writerow([student.StudentName,student.Class,student.Year, student.ParentNumber,student.StudentLocation, student.StatusFee, student.StatusFee_Semister_01, student.StatusFee_Semister_02, student.StatusFee_Semister_03, student.AmountRemained, student.AmountRemained_Semister_01, student.AmountRemained_Semister_02, student.AmountRemained_Semister_03 ])
            return response
            #ZINAISHIA HAPA ZA KUDOWNLOAD

            #HII NI CONTEXT KWA AJILI YA KUSEARCH ITEM OR CATEGORY KWENYE FORMYETU
        context ={
        #"QuerySet":QuerySet,
        "form":form,
        "queryset":queryset,
        "page":page,
        "className":className,
    }   

    return render(request, 'App/AllStudents.html',context)








#------------UPLOAD STUDENTS--------------
def UploadExcellFile(request):
    if request.method == "POST":
        try:
            item_resource = StudentsResource()
            dataset = Dataset()
            new_item_resource = request.FILES['myfile']

            if not new_item_resource.name.endswith('xlsx'):
                messages.info(request, 'wrong format')
                return render(request, 'App/UploadExcellFile.html')


            imported_data = dataset.load(new_item_resource.read(), format='xlsx')

            for data in imported_data:
                value = Students(
                    data[0], #ID
                    data[1], #StudentName
                    data[2], #Class
                    data[3], #Year
                    
                    data[4], #ParentNumber
                    data[5], #StudentLocation
                    data[6], #Gender
                    data[7],
                    data[8],
                    data[9],
                    data[10],
                    data[11],
                    data[12],
                    data[13],
                    data[14],
                    data[15],
                    data[16],
                    data[17],
                    data[18],
                    data[19],
                    data[20],
                    data[21],
                    data[22],
                    data[23],
                    data[24],
                    data[25],
                    data[26],
                    data[27],
                    data[28]

                    
                    # data[11], #Created
                    # data[12] #Updated
                    )
                value.save()
            messages.success(request, 'Data Uploaded successfully')

        except Exception as e:
            messages.error(request, f'Error uploading data: {str(e)}')

    return render(request, 'App/UploadExcellFile.html')














@login_required(login_url='login')
def search_student_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(StudentName__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = Students.objects.filter(search)
    mylist= []
    mylist += [x.StudentName for x in filters]
    return JsonResponse(mylist, safe=False)






def StudentDetailPage(request, id):
    queryset = Students.objects.get(id=id)
    
    context ={
        
        "queryset":queryset
    }
    
    
        

    return render(request, 'App/StudentDetailPage.html',context)


#RECEIVE FOR ALL SEMISTERS
def ReceiveStudentFee(request, id):
    queryset = Students.objects.get(id=id)
    studentId = queryset.id
    check_remained_amount_2 = 0
    check_remained_amount_1 = 0
    check_remained_amount_3 = 0
    saved_remained_amount_11 = 0
    saved_remained_amount_1 = 0
    saved_remained_amount_22 =0
    saved_remained_amount_2 = 0
    saved_remained_amount_33 = 0
    saved_remained_amount_3 = 0
    check_received_amount_all = 0
    

    form= ReceiveStudentFeeeForm(request.POST or None, instance=queryset)

    if form.is_valid():

        #mwanzo kwa ajili ya mwaka mzima    
        instance = form.save(commit=False)

        check_received_amount_all = instance.ReceivedAmount
        if check_received_amount_all < instance.Class.SemisterFee:
            messages.info(request, f"Kiasi ulichoingiza {instance.ReceivedAmount}  ni sawa au chini ya  ada ya semister husika {instance.Class.SemisterFee}. \n Tafadhali chagua  semister husika kuingiza malipo. ")
            return redirect('ReceiveStudentFee', id=id)


        instance.StatusFee += instance.ReceivedAmount
        instance.AmountRemained = instance.Class.ClassFee - instance.StatusFee
        instance.AmountExceed = instance.StatusFee - instance.Class.ClassFee
        instance.ReceivedBy = request.user.username
        
        
        Total_amount_paid = instance.StatusFee
        amount_remained = instance.AmountRemained
        amount_exceed = instance.AmountExceed
        total_fee = instance.Class.ClassFee

        if Total_amount_paid == total_fee:
            instance.is_finished = True

            #mwanzo kwa ajili ya first semister
            instance.StatusFee_Semister_01 = instance.Class.SemisterFee
            instance.AmountRemained_Semister_01 =instance.Class.SemisterFee -instance.Class.SemisterFee 
            
            instance.StatusFee_Semister_02 = instance.Class.SemisterFee
            instance.AmountRemained_Semister_02 =instance.Class.SemisterFee -instance.Class.SemisterFee 

            instance.StatusFee_Semister_03 = instance.Class.SemisterFee
            instance.AmountRemained_Semister_03 =instance.Class.SemisterFee -instance.Class.SemisterFee 

            instance.ReceivedBy = request.user.username

            instance.save()

        if instance.StatusFee < total_fee:
            
            if instance.ReceivedAmount >= instance.Class.SemisterFee:
                if instance.StatusFee_Semister_01 == 0:

                    instance.StatusFee_Semister_01 = instance.Class.SemisterFee
                    instance.AmountRemained_Semister_01 =instance.Class.SemisterFee -instance.Class.SemisterFee
                    check_remained_amount_1= instance.ReceivedAmount - instance.Class.SemisterFee
                    print(f"CHECK 1 {check_remained_amount_1}")

                else:
                    saved_remained_amount_1 = instance.Class.SemisterFee - instance.StatusFee_Semister_01
                    instance.StatusFee_Semister_01 += saved_remained_amount_1
                    instance.AmountRemained_Semister_01 =instance.Class.SemisterFee -instance.StatusFee_Semister_01
                    
                    saved_remained_amount_11 = instance.ReceivedAmount - saved_remained_amount_1
                    check_remained_amount_1 = saved_remained_amount_11

                #kwa semister ya pili
                
                print(f"CHECK 12 {check_remained_amount_2}")
                if check_remained_amount_1 >= instance.Class.SemisterFee:
                    if instance.StatusFee_Semister_02 == 0:

                        instance.StatusFee_Semister_02 = instance.Class.SemisterFee
                        instance.AmountRemained_Semister_02 =instance.Class.SemisterFee -instance.Class.SemisterFee
                        check_remained_amount_2 = check_remained_amount_1 -instance.Class.SemisterFee
                        print(f"CHECK 2 sawa 0 {check_remained_amount_2}")
                   
                    else:
                        saved_remained_amount_2 = instance.Class.SemisterFee - instance.StatusFee_Semister_02
                        instance.StatusFee_Semister_02 += saved_remained_amount_2
                        instance.AmountRemained_Semister_02 =instance.Class.SemisterFee -instance.StatusFee_Semister_02
                        
                        saved_remained_amount_22 = check_remained_amount_1 - saved_remained_amount_2
                        check_remained_amount_2 = saved_remained_amount_22

                        print(f"REMAINED AMOUNT 2 {check_remained_amount_2} ")

                    #kwa ajili ya semister 3
                    
                    if check_remained_amount_2 >= instance.Class.SemisterFee:
                        if instance.StatusFee_Semister_03 == 0:
                            instance.StatusFee_Semister_03 = instance.Class.SemisterFee
                            instance.AmountRemained_Semister_03 =instance.Class.SemisterFee -instance.Class.SemisterFee
                            check_remained_amount_3 = check_remained_amount_2 -instance.Class.SemisterFee
                            print(f"CHECK 3 {check_remained_amount_3}")

                        else:
                            saved_remained_amount_3 = instance.Class.SemisterFee - instance.StatusFee_Semister_03
                            instance.StatusFee_Semister_03 += saved_remained_amount_3
                            instance.AmountRemained_Semister_03 =instance.Class.SemisterFee -instance.StatusFee_Semister_03
                            
                            saved_remained_amount_33 = check_remained_amount_2 - saved_remained_amount_3
                            check_remained_amount_3 = saved_remained_amount_33

                            #kwasababu hatuna semister nyingine inayofuata tutateminate hapa
                            #na km kuna hela bado inaelea basi hiyo itakuwa amount iliyozidi
                            # na itaonekana kwenye semister ya mwisho
                            AmountExceed_Semister_03 = check_remained_amount_3

                    #hii ni else ya semister ya tatu km amount
                    # iliyobakia kwenye semister two ni ndogo
                    # ya amount ya ada ya semister 3
                    else:
                        #hii bloku yote ni kucheki
                        # km teyali kulikuwa na
                        #amount kwenye semister 3 au laah
                        if instance.StatusFee_Semister_03 == 0:
                            instance.StatusFee_Semister_03 = check_remained_amount_2
                            instance.AmountRemained_Semister_03 =instance.Class.SemisterFee - check_remained_amount_2

                        else:
                            saved_remained_amount_3 = instance.Class.SemisterFee - instance.StatusFee_Semister_03
                            instance.StatusFee_Semister_03 += saved_remained_amount_3
                            instance.AmountRemained_Semister_03 =instance.Class.SemisterFee -instance.StatusFee_Semister_03
                            
                            saved_remained_amount_33 = check_remained_amount_2 - saved_remained_amount_3
                            check_remained_amount_3 = saved_remained_amount_33

                            #kwasababu hatuna semister nyingine inayofuata tutateminate hapa
                            #na km kuna hela bado inaelea basi hiyo itakuwa amount iliyozidi
                            # na itaonekana kwenye semister ya mwisho
                            AmountExceed_Semister_03 = check_remained_amount_3
                
                #hii ni else ya semister ya pili km amount
                # iliyobakia kwenye semister one ni ndogo
                # ya amount ya ada ya semister 2         
                else:
                    if instance.StatusFee_Semister_02 == 0:

                        instance.StatusFee_Semister_02 = check_remained_amount_1
                        instance.AmountRemained_Semister_02 =instance.Class.SemisterFee - check_remained_amount_1

                        instance.StatusFee_Semister_03 = 0
                        instance.AmountRemained_Semister_03 =0

                    else:
                        saved_remained_amount_2 = instance.Class.SemisterFee - instance.StatusFee_Semister_02
                        instance.StatusFee_Semister_02 += saved_remained_amount_2
                        instance.AmountRemained_Semister_02 =instance.Class.SemisterFee -instance.StatusFee_Semister_02
                        
                        saved_remained_amount_22 = check_remained_amount_1 - saved_remained_amount_2
                        check_remained_amount_2 = saved_remained_amount_22


            #Hii ni kama kiasi alicholipa ni kidogo ya semister Fee
            else:
                instance.StatusFee_Semister_01 =instance.StatusFee
                instance.AmountRemained_Semister_01 =instance.Class.SemisterFee - instance.StatusFee

                instance.StatusFee_Semister_02 = 0
                instance.AmountRemained_Semister_02 =0

                instance.StatusFee_Semister_03 = 0
                instance.AmountRemained_Semister_03 =0

        if instance.StatusFee > total_fee:
            instance.StatusFee_Semister_01 = instance.Class.SemisterFee
            instance.AmountRemained_Semister_01 =instance.Class.SemisterFee -instance.Class.SemisterFee 
            
            instance.StatusFee_Semister_02 = instance.Class.SemisterFee
            instance.AmountRemained_Semister_02 =instance.Class.SemisterFee -instance.Class.SemisterFee 

            instance.StatusFee_Semister_03 = instance.Class.SemisterFee
            instance.AmountRemained_Semister_03 =instance.Class.SemisterFee -instance.Class.SemisterFee 
            
            instance.AmountExceed = instance.StatusFee - total_fee
            
            
              

            

       

        #messages.success(request,"Items Issued successfully. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in store")
        instance.save()
        messages.success(request, "Received successfully. " + "Tsh. " + str(instance.ReceivedAmount) + " " + str(instance.StudentName) + "/=")
        #return redirect('stock_detailpage/'+str(instance.id))
        return redirect('StudentDetailPage',id=id)
        #return HttpResponseRedirect(instance.get_absolute_url())
    context ={
        "instance":queryset,
        "form":form,
        "studentId":studentId,

        # "instance.StatusFee":Total_amount_paid,
        # "amount_remained":amount_remained,
        # "amount_exceed":amount_exceed,
        
        #"username": 'Issued By: ' + str(request.user),
        "title": 'Receive ' + str(queryset.StudentName),
    }
    
    
        

    return render(request, 'App/ReceiveStudentFee.html',context)





#RECEIVE FOR  SEMISTER 1
def ReceiveStudentFee_Semister_01(request, id):
    queryset = Students.objects.get(id=id)
    studentId = queryset.id
    

    form= ReceiveStudentFeeeForm(request.POST or None, instance=queryset)

    if form.is_valid():
        


        #mwanzo kwa ajili ya mwaka mzima    
        instance = form.save(commit=False)

        #make sure entered amount is not greater than semister fee
        check_received_amount_1 = instance.ReceivedAmount
        if check_received_amount_1 > instance.Class.SemisterFee:
            messages.info(request, f"Kiasi ulichoingiza {instance.ReceivedAmount}  ni kikubwa kuzidi ada ya semister husika {instance.Class.SemisterFee}. \n Tafadhali chagua another option => Total Fee \n Au ingiza kiasi husika kwa kila Muhula. ")
            return redirect('ReceiveStudentFee_Semister_01', id=id)

        check_semister_status_fee_amount_1 = instance.StatusFee_Semister_01 + instance.ReceivedAmount
        if check_semister_status_fee_amount_1 > instance.Class.SemisterFee:
            messages.info(request, f"Mwanafunzi alishalipa {instance.StatusFee_Semister_01}/=,  na anadaiwa {instance.AmountRemained_Semister_01}/=. \n Kiasi ulichoingiza kinazidi ada ya semister Tafadhali chagua another option => Total Fee \n Au ingiza kiasi husika kwa kila Muhula.")
            return redirect('ReceiveStudentFee_Semister_01', id=id)




        instance.StatusFee += instance.ReceivedAmount
        instance.AmountRemained = instance.Class.ClassFee - instance.StatusFee
        instance.AmountExceed = instance.StatusFee - instance.Class.ClassFee
        instance.ReceivedBy = request.user.username
        
        
        Total_amount_paid = instance.StatusFee
        amount_remained = instance.AmountRemained
        amount_exceed = instance.AmountExceed
        total_fee = instance.Class.ClassFee

        if Total_amount_paid == total_fee:
            instance.is_finished = True
            instance.save()
        #mwisho kwa ajili ya mwaka mzima


        #mwanzo kwa ajili ya first semister    
        
        instance.StatusFee_Semister_01 += instance.ReceivedAmount
        instance.AmountRemained_Semister_01 = instance.Class.SemisterFee - instance.StatusFee_Semister_01
        instance.AmountExceed = instance.StatusFee_Semister_01 - instance.Class.SemisterFee
        instance.ReceivedBy = request.user.username
        
        
        Total_amount_paid_Semister_01 = instance.StatusFee_Semister_01
        amount_remained_Semister_01 = instance.AmountRemained_Semister_01
        amount_exceed_Semister_01 = instance.AmountExceed_Semister_01
        total_fee_Semister_01 = instance.Class.SemisterFee

        if Total_amount_paid_Semister_01 == total_fee_Semister_01:
            instance.is_finished_Semister_01 = True
            instance.save()
        #mwisho kwa ajili ya first semiste

        

        #messages.success(request,"Items Issued successfully. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in store")
        instance.save()
        messages.success(request, "Received successfully. " + "Tsh. " + str(instance.ReceivedAmount)+"/=" + " " + str(instance.StudentName)  + " for semister 1")
        #return redirect('stock_detailpage/'+str(instance.id))
        return redirect('StudentDetailPage',id=id)
        #return HttpResponseRedirect(instance.get_absolute_url())
    context ={
        "instance":queryset,
        "form":form,
        "studentId":studentId,

        # "Total_amount_paid":Total_amount_paid,
        # "amount_remained":amount_remained,
        # "amount_exceed":amount_exceed,
        
        #"username": 'Issued By: ' + str(request.user),
        "title": 'Receive ' + str(queryset.StudentName),
    }
    
    
        

    return render(request, 'App/ReceiveStudentFee.html',context)





#RECEIVE FOR SEMISTER 02
def ReceiveStudentFee_Semister_02(request, id):
    queryset = Students.objects.get(id=id)
    studentId = queryset.id
    

    form= ReceiveStudentFeeeForm(request.POST or None, instance=queryset)

    if form.is_valid():

        #mwanzo kwa ajili ya mwaka mzima    
        instance = form.save(commit=False)

        #make sure entered amount is not greater than semister fee
        check_received_amount_2 = instance.ReceivedAmount
        if check_received_amount_2 > instance.Class.SemisterFee:
            messages.info(request, f"Kiasi ulichoingiza {instance.ReceivedAmount}  ni kikubwa kuzidi ada ya semister husika {instance.Class.SemisterFee}. \n Tafadhali chagua another option => Total Fee \n Au ingiza kiasi husika kwa kila Muhula. ")
            return redirect('ReceiveStudentFee_Semister_02', id=id)

        check_semister_status_fee_amount_2 = instance.StatusFee_Semister_02 + instance.ReceivedAmount
        if check_semister_status_fee_amount_2 > instance.Class.SemisterFee:
            messages.info(request, f"Mwanafunzi alishalipa {instance.StatusFee_Semister_02}/=,  na anadaiwa {instance.AmountRemained_Semister_02}/=. \n Kiasi ulichoingiza kinazidi ada ya semister Tafadhali chagua another option => Total Fee \n Au ingiza kiasi husika kwa kila Muhula.")
            return redirect('ReceiveStudentFee_Semister_02', id=id)


        instance.StatusFee += instance.ReceivedAmount
        instance.AmountRemained = instance.Class.ClassFee - instance.StatusFee
        instance.AmountExceed = instance.StatusFee - instance.Class.ClassFee
        instance.ReceivedBy = request.user.username
        
        
        Total_amount_paid = instance.StatusFee
        amount_remained = instance.AmountRemained
        amount_exceed = instance.AmountExceed
        total_fee = instance.Class.ClassFee

        if Total_amount_paid == total_fee:
            instance.is_finished = True
            instance.save()
        #mwisho kwa ajili ya mwaka mzima


        #mwanzo kwa ajili ya second semister    
        
        instance.StatusFee_Semister_02 += instance.ReceivedAmount
        instance.AmountRemained_Semister_02 = instance.Class.SemisterFee - instance.StatusFee_Semister_02
        instance.AmountExceed = instance.StatusFee_Semister_02 - instance.Class.SemisterFee
        instance.ReceivedBy = request.user.username
        
        
        Total_amount_paid_Semister_02 = instance.StatusFee_Semister_02
        amount_remained_Semister_02 = instance.AmountRemained_Semister_02
        amount_exceed_Semister_02 = instance.AmountExceed_Semister_02
        total_fee_Semister_02 = instance.Class.SemisterFee

        if Total_amount_paid_Semister_02 == total_fee_Semister_02:
            instance.is_finished_Semister_02 = True
            instance.save()
        #mwisho kwa ajili ya first semiste

        

        #messages.success(request,"Items Issued successfully. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in store")
        instance.save()
        messages.success(request, "Received successfully. " + "Tsh. " + str(instance.ReceivedAmount)+"/=" + " " + str(instance.StudentName)  + " for semister 2")
        #return redirect('stock_detailpage/'+str(instance.id))
        return redirect('StudentDetailPage',id=id)
        #return HttpResponseRedirect(instance.get_absolute_url())
    context ={
        "instance":queryset,
        "form":form,
        "studentId":studentId,

        # "Total_amount_paid":Total_amount_paid,
        # "amount_remained":amount_remained,
        # "amount_exceed":amount_exceed,
        
        #"username": 'Issued By: ' + str(request.user),
        "title": 'Receive ' + str(queryset.StudentName),
    }
    
    
        

    return render(request, 'App/ReceiveStudentFee.html',context)





#RECEIVE FOR SEMISTER 03
def ReceiveStudentFee_Semister_03(request, id):
    queryset = Students.objects.get(id=id)
    studentId = queryset.id
    

    form= ReceiveStudentFeeeForm(request.POST or None, instance=queryset)

    if form.is_valid():

        #mwanzo kwa ajili ya mwaka mzima    
        instance = form.save(commit=False)

        #make sure entered amount is not greater than semister fee
        check_received_amount_3 = instance.ReceivedAmount
        if check_received_amount_3 > instance.Class.SemisterFee:
            messages.info(request, f"Kiasi ulichoingiza {instance.ReceivedAmount}  ni kikubwa kuzidi ada ya semister husika {instance.Class.SemisterFee}. \n Tafadhali chagua another option => Total Fee \n Au ingiza kiasi husika kwa kila Muhula. ")
            return redirect('ReceiveStudentFee_Semister_03', id=id)

        check_semister_status_fee_amount_3 = instance.StatusFee_Semister_03 + instance.ReceivedAmount
        if check_semister_status_fee_amount_3 > instance.Class.SemisterFee:
            messages.info(request, f"Mwanafunzi alishalipa {instance.StatusFee_Semister_03}/=,  na anadaiwa {instance.AmountRemained_Semister_03}/=. \n Kiasi ulichoingiza kinazidi ada ya semister Tafadhali chagua another option => Total Fee \n Au ingiza kiasi husika kwa kila Muhula.")
            return redirect('ReceiveStudentFee_Semister_03', id=id)

        instance.StatusFee += instance.ReceivedAmount
        instance.AmountRemained = instance.Class.ClassFee - instance.StatusFee
        instance.AmountExceed = instance.StatusFee - instance.Class.ClassFee
        instance.ReceivedBy = request.user.username
        
        
        Total_amount_paid = instance.StatusFee
        amount_remained = instance.AmountRemained
        amount_exceed = instance.AmountExceed
        total_fee = instance.Class.ClassFee

        if Total_amount_paid == total_fee:
            instance.is_finished = True
            instance.save()
        #mwisho kwa ajili ya mwaka mzima


        #mwanzo kwa ajili ya third semister    
        
        instance.StatusFee_Semister_03 += instance.ReceivedAmount
        instance.AmountRemained_Semister_03 = instance.Class.SemisterFee - instance.StatusFee_Semister_03
        instance.AmountExceed = instance.StatusFee_Semister_03 - instance.Class.SemisterFee
        instance.ReceivedBy = request.user.username
        
        
        Total_amount_paid_Semister_03 = instance.StatusFee_Semister_03
        amount_remained_Semister_03 = instance.AmountRemained_Semister_03
        amount_exceed_Semister_03 = instance.AmountExceed_Semister_03
        total_fee_Semister_03 = instance.Class.SemisterFee

        if Total_amount_paid_Semister_03 == total_fee_Semister_03:
            instance.is_finished_Semister_03 = True
            instance.save()
        #mwisho kwa ajili ya third semiste

        

        #messages.success(request,"Items Issued successfully. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in store")
        instance.save()
        messages.success(request, "Received successfully. " + "Tsh. " + str(instance.ReceivedAmount)+"/=" + " " + str(instance.StudentName)  + " for semister 3")
        #return redirect('stock_detailpage/'+str(instance.id))
        return redirect('StudentDetailPage',id=id)
        #return HttpResponseRedirect(instance.get_absolute_url())
    context ={
        "instance":queryset,
        "form":form,
        "studentId":studentId,

        # "Total_amount_paid":Total_amount_paid,
        # "amount_remained":amount_remained,
        # "amount_exceed":amount_exceed,
        
        #"username": 'Issued By: ' + str(request.user),
        "title": 'Receive ' + str(queryset.StudentName),
    }
    
    
        

    return render(request, 'App/ReceiveStudentFee.html',context)

# class add_items(SuccessMessageMixin, CreateView):
#     model = Stock
#     template_name = 'App/AddNewStudent.html'
#     form_class = StudentCreateForm
#     success_url = reverse_lazy('AddNewStudent')
#     success_message = "Item added successfully in your stock"
# class update_items(SuccessMessageMixin, UpdateView):
#     model = Stock
#     template_name = 'DimosoApp/add_items.html'
#     form_class = StockUpdateForm
#     success_url = reverse_lazy('stock')
#     success_message = "Item updated successfully in your stock"


def AddNewStudent(request):
    form = StudentCreateForm()
    if request.method == "POST":
        StudentName = request.POST.get('StudentName')
        form = StudentCreateForm(request.POST or None, files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, f"Informations of {StudentName} were added successfully")
            return redirect('AddNewStudent')

        messages.success(request, f"Error adding new student")
        return redirect('AddNewStudent')


    context ={
        
        "form":form,
        
    }
    
    
        

    return render(request, 'App/AddNewStudent.html',context)


def UpdateStudent(request,id):
    x = Students.objects.get(id=id)
    form = StudentCreateForm(instance=x)
    if request.method == "POST":
        StudentName = request.POST.get('StudentName')
        form = StudentCreateForm(request.POST, files=request.FILES, instance=x)

        if form.is_valid():
            form.save()
            messages.success(request, f"Informations of {x.StudentName} were updated successfully")
            return redirect('AllClasses')

        messages.success(request, f"Error updating student")
        return redirect('AllClasses')


    context ={
        
        "form":form,
        
    }
    
    
        

    return render(request, 'App/UpdateStudent.html',context)



def DeleteStudent(request,id):
    x = Students.objects.get(id=id)
    x.delete()
    messages.success(request, f"Informations of {x.StudentName} were deleted successfully")
    return redirect('AllClasses')
    
    




def AddNewClass(request):
    form = AddNewClassForm()
    if request.method == "POST":
        ClassName = request.POST.get('ClassName')
        form = AddNewClassForm(request.POST or None, files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, f"Informations of {ClassName} were added successfully")
            return redirect('AddNewClass')

        messages.success(request, f"Error adding new class")
        return redirect('AddNewClass')


    context ={
        
        "form":form,
        
    }
    
    
        

    return render(request, 'App/AddNewClass.html',context)


def UpdateClass(request,id):
    x = Classes.objects.get(id=id)
    form = AddNewClassForm(instance=x)
    if request.method == "POST":
        ClassName = request.POST.get('ClassName')
        form = AddNewClassForm(request.POST, files=request.FILES, instance=x)

        if form.is_valid():
            form.save()
            messages.success(request, f"Informations of {x.ClassName} were updated successfully")
            return redirect('AllClasses')

        messages.success(request, f"Error updating class")
        return redirect('AllClasses')


    context ={
        
        "form":form,
        
    }
    
    
        

    return render(request, 'App/UpdateClass.html',context)



def DeleteClass(request,id):
    x = Classes.objects.get(id=id)
    x.delete()
    messages.success(request, f"Informations of {x.ClassName} were deleted successfully")
    return redirect('AllClasses')
  
        


def AddNewYear(request):
    form = AddNewYearForm()
    if request.method == "POST":
        Year = request.POST.get('Year')
        form = AddNewYearForm(request.POST or None, files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, f"Informations of {Year} were added successfully")
            return redirect('AddNewYear')

        messages.success(request, f"Error adding new class")
        return redirect('AddNewYear')


    context ={
        
        "form":form,
        
    }
    
    
        

    return render(request, 'App/AddNewYear.html',context)


def UpdateYear(request,id):
    x = Years.objects.get(id=id)
    form = AddNewYearForm(instance=x)
    if request.method == "POST":
        Year = request.POST.get('Year')
        form = AddNewYearForm(request.POST, files=request.FILES, instance=x)

        if form.is_valid():
            form.save()
            messages.success(request, f"Informations of {x.Year} were updated successfully")
            return redirect('AllYearsPage')

        messages.success(request, f"Error updating new student")
        return redirect('AllYearsPage')


    context ={
        
        "form":form,
        
    }
    
    
        

    return render(request, 'App/UpdateYear.html',context)



def DeleteYear(request,id):
    x = Years.objects.get(id=id)
    x.delete()
    messages.success(request, f"Informations of {x.Year} were deleted successfully")
    return redirect('AllYearsPage')













@login_required(login_url='login')
def AllPaidStudents(request):
    # classId = Classes.objects.get(id=id)
    # className = classId.ClassName

    form = StudentsSearchForm(request.POST or None)
    # x= datetime.now()
    # current_date = x.strftime('%d-%m-%Y %H:%M')
    

    queryset = Students.objects.filter(

            is_finished = True

        ).order_by('-id')


    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,10)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)
    
    form = StudentsSearchForm(request.POST or None)




    #MWISHO HAP




    context ={
        "queryset":queryset,
        "form":form,
        "page":page,
        # "current_date":current_date,
        
    }

    #kwa ajili ya kufilter items and category ktk form
    if request.method == 'POST':
        #category__icontains=form['category'].value(),
        Class = form['Class'].value()

        

                                        
        queryset = Students.objects.filter(
                                        StudentName__icontains=form['StudentName'].value(),
                                        is_finished = True

                                        #last_updated__gte=form['start_date'].value(),
                                        # last_updated__lte=form['end_date'].value()
                                        #last_updated__range=[
                                            #form['start_date'].value(),
                                            #form['end_date'].value()
                                        #]
            )
        if (Class != ''):
            queryset = Students.objects.filter(
                    is_finished = True
                )
            queryset = queryset.filter(Class_id=Class)

            #To SET  PAGINATION IN STOCK LIST PAGE
            paginator = Paginator(queryset,10)
            page = request.GET.get('page')
            try:
                queryset=paginator.page(page)
            except PageNotAnInteger:
                queryset=paginator.page(1)
            except EmptyPage:
                queryset=paginator.page(paginator.num_pages)
            #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI
        
        #hii ni kwa ajili ya kudownload ile page nzima ya stock endapo mtu akiweka tiki kwenye field export to csv
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['content-Disposition'] = 'attachment; filename="Students Details.csv"'
            writer = csv.writer(response)
            writer.writerow(['Student Name','Class', 'Year', 'Parent Number','Location', 'Total Amount Paid', 'Total Amount Paid Semister 1', 'Total Amount Paid Semister 2', 'Total Amount Paid Semister 3', 'Total Amount Remained', 'Amount Remained Semister 1', 'Amount Remained Semister 2', 'Amount Remained Semister 3'])
            instance = queryset
            for student in queryset:
                writer.writerow([student.StudentName,student.Class,student.Year, student.ParentNumber,student.StudentLocation, student.StatusFee, student.StatusFee_Semister_01, student.StatusFee_Semister_02, student.StatusFee_Semister_03, student.AmountRemained, student.AmountRemained_Semister_01, student.AmountRemained_Semister_02, student.AmountRemained_Semister_03 ])
            return response
            #ZINAISHIA HAPA ZA KUDOWNLOAD

            #HII NI CONTEXT KWA AJILI YA KUSEARCH ITEM OR CATEGORY KWENYE FORMYETU
        context ={
        #"QuerySet":QuerySet,
        "form":form,
        "queryset":queryset,
        "page":page,
        
    }   

    return render(request, 'App/AllPaidStudents.html',context)
    





@login_required(login_url='login')
def AllUnPaidStudents(request):
    # classId = Classes.objects.get(id=id)
    # className = classId.ClassName

    form = StudentsSearchForm(request.POST or None)
    # x= datetime.now()
    # current_date = x.strftime('%d-%m-%Y %H:%M')
    

    queryset = Students.objects.filter(
            is_finished = False

            

        ).order_by('-id')


    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,10)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)
    
    form = StudentsSearchForm(request.POST or None)




    #MWISHO HAP




    context ={
        "queryset":queryset,
        "form":form,
        "page":page,
        # "current_date":current_date,
        
    }

    #kwa ajili ya kufilter items and category ktk form
    if request.method == 'POST':
        #category__icontains=form['category'].value(),
        Class = form['Class'].value()

        

                                        
        queryset = Students.objects.filter(
                                        StudentName__icontains=form['StudentName'].value(),
                                        is_finished = False

                                        #last_updated__gte=form['start_date'].value(),
                                        # last_updated__lte=form['end_date'].value()
                                        #last_updated__range=[
                                            #form['start_date'].value(),
                                            #form['end_date'].value()
                                        #]
            )
        if (Class != ''):
            queryset = Students.objects.filter(
                    is_finished = False
                )
            queryset = queryset.filter(Class_id=Class)

            #To SET  PAGINATION IN STOCK LIST PAGE
            paginator = Paginator(queryset,10)
            page = request.GET.get('page')
            try:
                queryset=paginator.page(page)
            except PageNotAnInteger:
                queryset=paginator.page(1)
            except EmptyPage:
                queryset=paginator.page(paginator.num_pages)
            #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI
        
        #hii ni kwa ajili ya kudownload ile page nzima ya stock endapo mtu akiweka tiki kwenye field export to csv
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['content-Disposition'] = 'attachment; filename="Students Details.csv"'
            writer = csv.writer(response)
            writer.writerow(['Student Name','Class', 'Year', 'Parent Number','Location', 'Total Amount Paid', 'Total Amount Paid Semister 1', 'Total Amount Paid Semister 2', 'Total Amount Paid Semister 3', 'Total Amount Remained', 'Amount Remained Semister 1', 'Amount Remained Semister 2', 'Amount Remained Semister 3'])
            instance = queryset
            for student in queryset:
                writer.writerow([student.StudentName,student.Class,student.Year, student.ParentNumber,student.StudentLocation, student.StatusFee, student.StatusFee_Semister_01, student.StatusFee_Semister_02, student.StatusFee_Semister_03, student.AmountRemained, student.AmountRemained_Semister_01, student.AmountRemained_Semister_02, student.AmountRemained_Semister_03 ])
            return response
            #ZINAISHIA HAPA ZA KUDOWNLOAD

            #HII NI CONTEXT KWA AJILI YA KUSEARCH ITEM OR CATEGORY KWENYE FORMYETU
        context ={
        #"QuerySet":QuerySet,
        "form":form,
        "queryset":queryset,
        "page":page,
        
    }   

    return render(request, 'App/AllUnPaidStudents.html',context)