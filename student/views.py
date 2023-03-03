from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
import time

# Planning
# disable right click
# Send srcreen shot to admin when warning occurs

# Create your views here.
@login_required(login_url='login_page')
def assessment_page(request):
    if request.user.is_superuser:
        return HttpResponse('You are logged in as an admin, log in as student to view this page')

    if not hasAccessToAssessment(request):
        return HttpResponse("Access is denied, as you may have already submitted the test or you dont have access to view this page")

    try:
        test = Test.objects.get(is_ongoing=True)
    except:
        return HttpResponse('Test does not exist')
    
    questions = Question.objects.filter(test_id=test)
    options = Option.objects.all()
    customuser = CustomUser.objects.get(user=request.user)
    student_markings = StudentMarking.objects.filter(user=customuser)
    question_images = QuestionImage.objects.all()

    student_marking_options = []

    if customuser.is_banned:
        return HttpResponse('You are account is banned, kindly contact admin for further information')

    for q in questions:
        for o in options:
            if o.question_id == q: # Option is there for the current test
                for s_mark in student_markings:
                    if s_mark.option == o:
                        student_marking_options.append(s_mark.option)

    print("My list is : ",student_marking_options)


    if request.method == 'POST':
        enableSubmit(request)
        return redirect('student:end_page')

    context = {
        'test':test,
        'questions':questions,
        'options':options,
        'student_markings':student_markings,
        'student_marking_options':student_marking_options,
        'question_images':question_images,
    }
    return render(request,'student/assessment.html',context)

@login_required(login_url='login_page')
def check_compatibility_page(request):
    try:
        test = Test.objects.get(is_ongoing=True)
    except:
        return HttpResponse('Test has not yet begun, try again later')
    context = {}
    return render(request,'student/check_compatibility.html',context)

@login_required(login_url='login_page')
def rules_page(request):
    try:
        test = Test.objects.get(is_ongoing=True)
    except:
        return HttpResponse('Test has not yet begun, try again later')
    context = {}
    return render(request,'student/rules.html',context)

@login_required(login_url='login_page')
def end_page(request):
    context = {}
    return render(request,'student/end.html',context)


# Custom functions
# Function to check if user allowed to take the test
@login_required(login_url='login_page')
def hasAccessToAssessment(request):
    user = request.user
    # print("Type of user: ",user)
    customuser = CustomUser.objects.get(user=user)
    test = None

    try:
        test = Test.objects.get(is_ongoing=True)
    except:
        pass

    if test is []:    # If test not present
        print("No ongoing test found")
        return False
    else:
        # Check if user allowed in TestPermissions
        # Return true is user has permission else return false
        
        try:
            test_permission = TestPermission.objects.get(test_id=test,user=customuser)
            print("has testing permit")
        except:
            print("Some error occurred")
            return False

        # If result already exist for same test, then no access
        try:
            result = Result.objects.get(user=customuser,test_id=test.id)
            print("Result is already there")
            return False
        except: # means user has not submitted yet, so he has access to the test
            return True
        return True
    return False

@login_required(login_url='login_page')
def evaulate_result(request):
    customuser = CustomUser.objects.get(user=request.user)
    test = Test.objects.get(was_ongoing=True)
    pass_perc = int(test.pass_percentage)
    questions = Question.objects.filter(test_id=test)
    max_marks = 0
    obtained_marks = 0
    obtained_perc = 0

    # To get the total marks info
    for question in questions:
        max_marks = max_marks + int(question.marks)    

    student_marking_options = StudentMarking.objects.filter(user=customuser)

    print("Student marking options: ",student_marking_options,'Length is ',len(student_marking_options))
    for opt in student_marking_options:
        option = Option.objects.get(id=opt.option.id)
        
        print("Printing option : ",option)
        if option.question_id.test_id.id == test.id:
            if option.is_correct:        
                print("Option is ",option.option," Correct answer")        
                obtained_marks += int(question.marks)
            else:
                print("Option not correct")
        else:
            print("Option does not belong to the test")

    
    obtained_perc = (obtained_marks / max_marks) * 100

    print("Max marks is ",max_marks)
    print("Obtained marks is ",obtained_marks)
    print("Obtained perc is ",obtained_perc,' pass perc is ',pass_perc)
    
    if obtained_perc >= pass_perc:
        outcome = True
    else:
        outcome = False

    try:
        result = Result.objects.get(user=customuser,test_id=test)
        result.score = obtained_marks
        result.outcome = outcome
        result.save()
    except:
        result = Result.objects.create(user=customuser,test_id=test,score=obtained_marks,outcome=outcome)

    print('successfully entered into results model')
    return

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

# Json request functions used to get data from js using ajax
@login_required(login_url='login_page')
def saveOption(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    
    customuser = CustomUser.objects.get(user=request.user)
    try: # If already submitted then disable save feature
        results = Result.objects.get(user=customuser)
        return HttpResponse("Already submitted, try again later")
    except:
        pass

    if is_ajax(request=request):
        print("Got ajax request")
        option_id = request.GET.get('option_id')
        print("Recieved successful ,option_id: ",option_id)

        test = Test.objects.get(is_ongoing=True)
        option = Option.objects.get(id=option_id)

        # Work in progress
        try:
            student_marking = StudentMarking.objects.get(user=customuser,option=option)
            student_marking.option = option
        except StudentMarking.DoesNotExist:
            # If it doesnt exist then create it
            q_id = Question.objects.get(id=option.question_id.id)
            student_markings = StudentMarking.objects.filter(user=customuser)

            for s in student_markings:
                if s.option.question_id == q_id:
                    print("Existing data found, performing delete")
                    s.delete()

            student_marking = StudentMarking.objects.create(user=customuser,option=option)
    return JsonResponse({'data':[]},safe=False)

@login_required(login_url='login_page')
def get_remaining_duration(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    
    if is_ajax(request=request):
        try:
            test = Test.objects.get(was_ongoing=True)
        except:
            print('Returned :','None' )
            return JsonResponse({'data':'None'},safe=False)

        # print('test duration in python ',test.test_duration)
        test_duration_sec = int(test.test_duration) * 60
        
        start_time = test.started_at #Start time has to be taken from the database, change this later
        current_time = datetime.now().strftime('%H:%M:%S')

        t1 = datetime.strptime(start_time,"%H:%M:%S")
        # print('start time: ',t1.time())

        t2 = datetime.strptime(current_time,'%H:%M:%S')
        # print('current time: ',t2.time())

        delta = t2 - t1
        delta_total_sec = delta.total_seconds()

        # print("Duration in seconds : ",test_duration_sec)
        # print("difference in seconds ",delta_total_sec)

        final_diff = test_duration_sec - delta_total_sec
        print("Remaining seconds : ",final_diff)

        # print('final difference: ',final_diff)
        if final_diff < 5:
            final_diff = 'None'

        return JsonResponse({'data':final_diff},safe=False)

    return HttpResponse('Not good request')

@login_required(login_url='login_page')
def enableSubmit(request):
    customuser = CustomUser.objects.get(user=request.user)

    try:
        test = Test.objects.get(was_ongoing=True)
    except:
        return HttpResponse("Test not found")
    
    print(test)
    try:
        result = Result.objects.get(user=customuser,test_id=test)
        return HttpResponse("Data is already submitted in the results model")
    except Result.DoesNotExist:
        evaulate_result(request)
        return redirect('student:end_page')

def is_user_banned(request):
    if is_ajax(request=request):
        user = User.objects.get(id=request.user.id)
        customuser = CustomUser.objects.get(user=user)
        
        if customuser.is_banned:
            return JsonResponse({'data':'True'},safe=False)            
    return JsonResponse({'data':'False'},safe=False)

def ban_user(request):
    user = User.objects.get(id=request.user.id)
    customuser = CustomUser.objects.get(user=user)
    ban_detail = request.GET.get('ban_detail')
    print('Ban user in student module getting called')
    
    if customuser.is_banned:
        return JsonResponse({'data':'already banned'})

    customuser.is_banned = True
    customuser.save()

    test = Test.objects.get(is_ongoing=True)
    
    try:
        ban = Ban.objects.get(test_id=test,user=customuser)
        ban.ban_detail = ban_detail
        ban.ban_count = int(ban.ban_count)+1
        ban.save()
    except:
        ban = Ban.objects.create(test_id=test,user=customuser,ban_detail=ban_detail,ban_count=1)

    return JsonResponse({'data':''},safe=False)