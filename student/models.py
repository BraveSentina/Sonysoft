from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Test(models.Model):
    test_name = models.CharField(max_length=100,null=True,blank=True)
    test_duration = models.CharField(max_length=100,null=True,blank=True)
    is_ongoing = models.BooleanField(default=False)
    was_ongoing = models.BooleanField(default=False)
    is_register_allowed = models.BooleanField(default=False)
    pass_percentage = models.CharField(max_length=100,null=True,blank=True,default=70)
    created_on = models.DateField(auto_now_add=True)
    started_at = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.test_name

class TestPermission(models.Model):
    test_id = models.ForeignKey(Test,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.user.username

class Question(models.Model):
    test_id = models.ForeignKey(Test,on_delete=models.CASCADE)
    question = models.CharField(max_length=500,null=True,blank=True)
    marks = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.question

class QuestionImage(models.Model):
    question_id = models.ForeignKey(Question,on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True,upload_to='images/q_images')

    def __str__(self):
        return self.question_id.question

class Option(models.Model):
    option = models.CharField(max_length=100,null=True,blank=True)
    is_correct = models.BooleanField(default=False)
    question_id = models.ForeignKey(Question,on_delete=models.CASCADE)

    def __str__(self):
        return self.option

class Result(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    test_id = models.ForeignKey(Test,on_delete=models.CASCADE)
    score = models.CharField(max_length=100,null=True,blank=True)
    outcome = models.BooleanField(default=False)

    def __str__(self):
        return self.user.user.username

class StudentMarking(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    option = models.ForeignKey(Option,on_delete=models.CASCADE)


    def __str__(self):
        return self.user.user.username

class Ban(models.Model):
    test_id = models.ForeignKey(Test,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    ban_detail = models.CharField(max_length=100,null=True,blank=True)
    ban_count = models.CharField(max_length=100,null=True,blank=True,default='0')
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.user.username
