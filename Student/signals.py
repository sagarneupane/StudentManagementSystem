from django.dispatch import receiver
from .models import *
from django.db.models.signals import post_save, pre_delete,post_delete,pre_save


# Signals For ASSIGNMENT DETAILS
@receiver(pre_delete,sender=Assignment)

def post_save_assignment(sender,instance,*args,**kwargs):
    print("I am Before Deleting")
    """Clean Old Image Files"""
    
    try:
        instance.assigned_data.delete(save=False)
    except:
        pass

@receiver(pre_save,sender=Assignment)
def pre_save_assignment(sender,instance,*args,**kwargs):
    print("I am After Saving")
    try:
        old_data = instance.__class__.objects.get(id=instance.id).assigned_data.path
        try:
            new_data = instance.assigned_data.path
        except:
            new_data = old_data
        if new_data!=old_data:
            import os
            if os.path.exists(old_data):
                os.remove(old_data)
                
    except:
        pass
    
# Signals For STUDENT_DETAILS 
@receiver(pre_delete,sender=Student_Details)
def post_delete_Student(sender,instance,*args,**kwargs):
    print("I am Before Deleting")
    """Clean Old Image Files"""
    
    try:
        instance.image.delete(save=False)
    except:
        pass

@receiver(pre_save,sender=Student_Details)
def pre_save_Student(sender,instance,*args,**kwargs):
    print("I am After Saving")
    try:
        old_data = instance.__class__.objects.get(id=instance.id).image.path
        try:
            new_data = instance.image.path
        except:
            new_data = old_data
        if new_data!=old_data:
            import os
            if os.path.exists(old_data):
                os.remove(old_data)
                
    except:
        pass


# For Teacher DETAILS
@receiver(post_delete,sender=Teacher_Details)
def post_delete_Teacher(sender,instance,*args,**kwargs):
    
    try:
        instance.image.delete(save=False)
    except:
        pass
    
@receiver(pre_save,sender=Teacher_Details)
def pre_save_Teacher(sender,instance,*args,**kwargs):
    
    try:
        old_data = instance.__class__.objects.get(id=instance.id).image.path
        try:
            new_data = instance.image.path
        except:
            new_data = old_data
        if new_data!=old_data:
            import os 
            if os.path.exists(old_data):
                os.remove(old_data)
            
    except:
        pass


# Assignment By Student
  
@receiver(pre_delete,sender=SubmitAssignment)
def post_delete_submitassignment(sender,instance,*args,**kwargs):
    try:
        instance.submitted_data.delete(save=False)

    except:
        pass
    
@receiver(pre_save,sender=SubmitAssignment)
def pre_save_submitassignment(sender,instance,*args,**kwargs):
    try:
        print("hello World From Pre_save")
        old_data = instance.__class__.objects.get(id=instance.id).submitted_data.path
        edited = instance.__class__.objects.get(id=instance.id).edited
        edited = edited + 1 
        instance.edited = edited
        # SubmitAssignment.filter(pk=instance.pk).update(edited=edited)
        # print(old_data)
        try:
            new_data = instance.submitted_data.path
        except:
            new_data = old_data
        if new_data!=old_data:
            import os
            if os.path.exists(old_data):
                os.remove(old_data)
    except:
        pass



@receiver(pre_delete,sender=CorrectAnswer)
def pre_delete_correctAnswer(sender,instance,*args,**kwargs):
    try:
        
        instance.correct_answer.delete(save=False)
    except:
        pass

@receiver(pre_save,sender=CorrectAnswer)
def pre_save_correctAnswer(sender,instance,*args,**kwargs):
    try:
        print("Yes I am Pre Svae")
        old_data = instance.__class__.objects.get(id=instance.id).correct_answer.path
        print("hello world",old_data)
        try:
            new_data = instance.correct_answer.path
            print("inside Try")
        except:
            new_data = old_data
            print("Inside except")
        if new_data!=old_data:
            import os
            print("Hello insied if case")
            if os.path.exists(old_data):
                os.remove(old_data)
    except:
        pass
        