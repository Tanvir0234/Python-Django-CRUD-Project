from django.shortcuts import render,redirect
from .models import * 
from .forms import *

# Create your views here.
def showTrainee(request):
    trainees = Trainee.objects.all()
    return render(request,"show.html",{'trainees':trainees})
    
def saveTrainee(request):
    if request.method == 'POST':
      form = TraineeForm(request.POST)
      if form.is_valid():
        try:
            form.save()
            return redirect("/")
        except:
            pass 
      else:
        pass
    
    else:
        form = TraineeForm()
        
    return render(request,"trainee.html",{'form':form})    
    
def deleteTrainee(request,id):
    trainee = Trainee.objects.get(TraineeId = id)
    trainee.delete()
    return redirect('/')


def editTrainee(request,id):
    trainee = Trainee.objects.get(TraineeId = id) 
    return render(request,'edit.html',{'trainee':trainee})
    
       
def updateTrainee(request,id):
      trainee = Trainee.objects.get(TraineeId = id)           
      form = TraineeForm(request.POST , instance=trainee)
      if form.is_valid():
        try:
            form.save()
            return redirect("/")
        except:
            pass 
      else:
        pass

        