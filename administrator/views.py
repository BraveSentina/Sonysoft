from django.shortcuts import render,redirect
from student.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from student.models import *
from student import views as student_views
from datetime import datetime
import time
import os

# Create your views here.
@login_required(login_url='login_page')
def dashboard_page(request):
    if not request.user.is_superuser:
        return HttpResponse('You are not authenticated to view this page')

    date_and_time = datetime.today()
    test_permissions = None
    try:
        test = Test.objects.get(is_register_allowed=True)
        test_permissions = TestPermission.objects.filter(test_id=test)
    except:
        pass
    context = {
        'date_and_time': date_and_time,
        'is_any_test_ongoing':is_any_test_ongoing(request),
        'test_permissions':test_permissions,
    }
    return render(request,'administrator/dashboard.html',context)

@login_required(login_url='login_page')
def logs_page(request):
    if not request.user.is_superuser:
        return HttpResponse('You are not authenticated to view this page')

    context = {}
    return render(request,'administrator/logs.html',context)

@login_required(login_url='login_page')
def view_all_tests_page(request):
    if not request.user.is_superuser:
        return HttpResponse('You are not authenticated to view this page')

    tests = Test.objects.all().order_by('created_on')

    context = {
        'tests':tests,
    }
    return render(request,'administrator/view_all_tests.html',context)

@login_required(login_url='login_page')
def test_creator_page(request):
    if not request.user.is_superuser:
        return HttpResponse('You are not authenticated to view this page')

    if request.method == 'POST':
        test_name = request.POST.get('test_name')
        test_duration = request.POST.get('test_duration')
        pass_percentage = request.POST.get('pass_percentage')
        
        if test_name == '' or test_duration == '' or pass_percentage == '':
            return HttpResponse('Kindly provide a valid data')

        # Get current time
        current_time = datetime.now().strftime('%H:%M:%S')
        t2 = datetime.strptime(current_time,'%H:%M:%S')
        print('current time: ',t2.time())

        try:  
            test = Test.objects.create(test_name=test_name,test_duration=test_duration,pass_percentage=pass_percentage,started_at=t2.time())
            print('trying to create')
        except:
            return HttpResponse('some error occurred while creating test')
        return redirect('administrator:test_creator_page')

    tests = Test.objects.all().order_by('created_on').reverse()
    register_allowed_test = None
    try:
        register_allowed_test = Test.objects.get(is_register_allowed=True)
    except:
        pass

    context = {
        'tests':tests,
        'register_allowed_test':register_allowed_test,
        'is_any_test_ongoing':is_any_test_ongoing(request),

    }
    return render(request,'administrator/test_creator.html',context)

@login_required(login_url='login_page')
def monitor_page(request):
    if not request.user.is_superuser:
        return HttpResponse('You are not authenticated to view this page')
    
    test = None
    try:
        test = Test.objects.get(is_ongoing=True)
    except:
        return HttpResponse('No test is ongoing')

    bans = Ban.objects.filter(test_id=test)

    context = {
        'bans':bans,
    }
    return render(request,'administrator/monitor.html',context)

@login_required(login_url='login_page')
def results_page(request,test_id):
    if not request.user.is_superuser:
        return HttpResponse('You are not authenticated to view this page')

    test = None
    results = None

    try:
        test = Test.objects.get(id=test_id)
    except:
        return HttpResponse('Test does not exist')

    try:
        results = Result.objects.filter(test_id=test)
    except:
        return HttpResponse('Error occurred while fetching the results')
    
    questions = Question.objects.filter(test_id=test)
    marks = 0
    for question in questions:
        marks = marks +  int(question.marks)

    print('result is ',results)
    context = {
        'test':test,
        'results':results,
        'marks':marks,
    }
    return render(request,'administrator/results.html',context)

@login_required(login_url='login_page')
def test_editor_page(request,test_id,q_id):
    is_new_question = False
    test = Test.objects.get(id=test_id)
    question = None
    questions = None
    options = None
    question_images = None

    if not request.user.is_superuser:
        return HttpResponse('You are not authenticated to view this page')

    if is_test_ongoing(request,test_id):
        return HttpResponse('Test is in progress, cannot edit page')

    if is_already_attended(request,test_id):
        return HttpResponse('Test already attended, cannot modify')
    

    try:
        questions = Question.objects.filter(test_id=test_id)
    except Question.DoesNotExist:
        questions = None
    
    try:
        options = Option.objects.all()
    except Option.DoesNotExist:
        options = None

    if q_id != 'default':
        print('Loading from the database')

        try:
            question = Question.objects.get(test_id=test_id,id=q_id)
            options = Option.objects.filter(question_id=question)
            try:
                question_images = QuestionImage.objects.filter(question_id=question)
                print('question_images is ',question_images)
            except:
                pass

        except:
            return HttpResponse('Your requested page could not be found')     
    else:
        print('This is a new question')
        is_new_question = True


    if request.method == 'POST':
        q = request.POST.get('question')
        q_image = request.FILES.get('question_image')
        option_list = request.POST.getlist('option_text')
        correct_option = request.POST.get('correct_option')
        m = request.POST.get('marks')

        print('question is ',q)
        print('question image is ',q_image)
        print('option list is ',option_list)
        print('correct option is ',correct_option)
        print('marks is ',m)

        # Validate image
        if q_image != None:
            if validateImages(q_image) == False:
                print('image invalid is : ',q_image)
                return HttpResponse('Image format is invaid')

        hidden_q_id = request.POST.get('question_id')
        if hidden_q_id != None: #If old question then just update
            try:
                print('Trying update question id is : ',hidden_q_id)
                question = Question.objects.get(id=hidden_q_id)
                if question.question != q:
                    question.question = q
                    question.save() 
            
                if question.marks != m:
                    question.marks = m
                    question.save()
            except:
                return HttpResponse('Question retieval failed')

            try:
                if q_image != None:
                    question_images = QuestionImage.objects.create(question_id=question,image=q_image)

            except:
                return HttpResponse('Image creation failed')

            # Create new option if does not exist
            try:
                existing_options = Option.objects.filter(question_id=question)
                for opt in option_list:
                    is_present = False

                    for exis_opt in existing_options:
                        if opt == exis_opt.option:
                            is_present = True
                    if is_present == False:
                        Option.objects.create(question_id=question,option=opt)

            except:
                return HttpResponse('Option updation failed')
     
            return redirect('administrator:test_editor_page',test_id,q_id)
        print('exe till here')
        try:
            test = Test.objects.get(id=test_id)
            question = Question.objects.create(test_id=test,question=q,marks=m)
            
            for i in range(0,len(option_list)):
                if i == int(correct_option):
                    option = Option.objects.create(option=option_list[i],question_id=question,is_correct=True)
                else:
                    option = Option.objects.create(option=option_list[i],question_id=question)

            print('Success till here')
            if q_image != None:
                images = QuestionImage.objects.create(question_id=question,image=q_image)

            # return redirect('administrator:test_editor_page',test_id=test.id,q_id='default')
        except:
            return  HttpResponse('Some error ocurred while saving the question')    

    context = {
        'is_new_question':is_new_question,
        'question':question,
        'options':options,        
        'questions':questions,
        'question_images':question_images,
        'test_id':test_id,
        'is_any_test_ongoing':is_any_test_ongoing(request),
    }
    return render(request,'administrator/test_editor.html',context)

@login_required(login_url='login_page')
def test_permission(request):
    username = request.GET.get('username')
    print('username is : ',username)
    context = {}

    user = None
    customuser = None
    test = None
    has_permit = None

    if username != '':
        try:
            user = User.objects.get(username=username)
            customuser = CustomUser.objects.get(user=user)
        except:
            pass

        try:
            test = Test.objects.get(is_register_allowed=True)
        except:
            return HttpResponse('Register a test to proceed')

        try:
            test_permission = TestPermission.objects.get(user=customuser,test_id=test)
            has_permit = True
        except:
            has_permit = False
            
    context = {
        'user':customuser,
        'has_permit':has_permit,
    }
    return render(request,'administrator/test_permission.html',context)


# Functions

def delete_test(request,id):
    if not request.user.is_superuser:
        return HttpResponse('You are not authenticated to view this page')

    try:
        test = Test.objects.get(id=id)
        if is_test_ongoing(request,id):
            return HttpResponse('Test is in progress, cannot perform any operation')
        print('Succeess before delete')
        test.delete()
    except:
        return HttpResponse("Some error occurred while deleting test")
    return redirect('administrator:test_creator_page')

def validateImages(image):
    extensions = ['jpeg','jpg','png']
    file_extension = str(image).split('.')[-1]

    if file_extension in extensions:
        pass
    else:
        return False

def delete_all_question_images(request,test_id,q_id):
    if not request.user.is_superuser:
        return HttpResponse('You are not authenticated to view this page')

    if is_any_test_ongoing(request):
        return HttpResponse('Test is in progress, cannot perform any operation')

    if q_id == 'default':
        return redirect('administrator:test_editor_page',test_id,q_id)
    
    question = Question.objects.get(id=q_id)
    question_images = QuestionImage.objects.filter(question_id=question.id)

    print('Deletion got called')
    print('images to be deleted: ',question_images)

    for question_image in question_images:
        os.remove(question_image.image.path)
        question_image.delete()

    return redirect('administrator:test_editor_page',test_id,q_id)

def delete_option(request,test_id,q_id,option_id):
    if not request.user.is_superuser:
        return HttpResponse('You are not authenticated to view this page')

    question = Question.objects.get(id=q_id)
    option = Option.objects.get(question_id=question,id=option_id)
    option.delete()
    return redirect('administrator:test_editor_page', test_id, q_id)

def delete_question(request,q_id):
    if not request.user.is_superuser:
        return HttpResponse('You are not authenticated to view this page')

    try:
        question = Question.objects.get(id=q_id)
        question.delete()
        return redirect('administrator:test_editor_page',question.test_id.id,'default')
    except:
        return HttpResponse('Deletion of question failed')

def set_is_ongoing_to_true(request,test_id):
    if not request.user.is_superuser:
        return HttpResponse('You are not authenticated to view this page')

    test = None
    try:
        test = Test.objects.get(id=test_id)
    except:
        return HttpResponse('Test does not exist')

    all_tests = Test.objects.filter(is_ongoing=True)
    for t in all_tests:
        t.is_ongoing = False
        t.was_ongoing = False
        t.save()
        
    all_tests = Test.objects.filter(was_ongoing=True)
    for t in all_tests:
        t.is_ongoing = False
        t.was_ongoing = False
        t.save()
    
    current_time = datetime.now().strftime('%H:%M:%S')
    t2 = datetime.strptime(current_time,'%H:%M:%S')
    
    test.is_ongoing = True
    test.was_ongoing = True
    test.started_at = t2.time()
    test.save()
    return redirect('administrator:test_creator_page')

def is_any_test_ongoing(request):
    if not request.user.is_superuser:
        return HttpResponse('You are not authenticated to view this page')

    try:
        test = Test.objects.get(is_ongoing=True)
        return True
    except:
        return False
    return False

def is_test_ongoing(request,test_id):
    if not request.user.is_superuser:
        return HttpResponse('You are not authenticated to view this page')

    test = Test.objects.get(id=test_id)

    if test.is_ongoing:
        return True
    else:
        return False

def reset_is_ongoing_to_false(request):
    if not request.user.is_superuser:
        return HttpResponse('You are not authenticated to view this page')
    test = None
    try:
        test = Test.objects.get(is_ongoing=True)
    except:
        return redirect('administrator:test_creator_page')

    test.is_ongoing = False
    test.was_ongoing = True
    test.is_register_allowed = False
    test.save()
    return JsonResponse({'data':'None'},safe=False)

def is_already_attended(request,test_id):
    test = Test.objects.get(id=test_id)
    result = Result.objects.filter(test_id=test)

    if len(result) > 0:
        print('result is ',result)
        return True    
    return False

def allow_registeration(request,test_id):
    if is_any_test_ongoing(request):
        return HttpResponse('Test is ongoing, cannot perform any modification')
        
    try:
        tests = Test.objects.filter(is_register_allowed=True)

        for t in tests:
            t.is_register_allowed = False
            t.save()

        test = Test.objects.get(id=test_id)

        if is_already_attended(request,test_id):
            return HttpResponse('Cannot register again , as its already over')

        test.is_register_allowed = True
        test.save()
    except:
        return HttpResponse('Test not found')
    return redirect('administrator:test_creator_page')

def grant_or_revoke_test_permission(request,username):
    if not request.user.is_superuser:
        return HttpResponse('You are not allowed to view this page')
    
    user = None
    customuser = None
    test = None
    try:
        user = User.objects.get(username=username)
        customuser = CustomUser.objects.get(user=user)
    except:
        return HttpResponse('User does not exist')

    try:
        test = Test.objects.get(is_register_allowed=True)
    except:
        return HttpResponse('No test registered yet, register a test to proceed')

    try:
        test_permission = TestPermission.objects.get(user=customuser,test_id=test)
        test_permission.delete()
        print('removed permit for user, ',user)
    except:
        test_permission = TestPermission.objects.create(user=customuser,test_id=test)
        print('Access granted for user, ',user)

    return redirect('administrator:test_permission_page')

# def ban_user(request,user_id):
    # customuser = None
    # try:
    #     customuser = CustomUser.objects.get(id=user_id)
    # except:
    #     return HttpResponse('User could not be found when trying to ban')

    # # customuser.is_banned = True
    # # customuser.save()
    # print('user ban called')
    # return redirect('administrator:monitor_page')

def remove_ban(request,user_id):
    user = CustomUser.objects.get(id=user_id)
    user.is_banned = False
    user.save()
    return redirect('administrator:monitor_page')

def is_any_test_ongoing_json(request):
    if not request.user.is_superuser:
        return JsonResponse({'data':'No'},safe=False)

    try:
        test = Test.objects.get(is_ongoing=True)
        return JsonResponse({'data':'True'},safe=False)
    except:
        return JsonResponse({'data':'False'},safe=False)
    return JsonResponse({'data':'False'},safe=False)