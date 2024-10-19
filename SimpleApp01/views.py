from django.shortcuts import render,redirect
from .models import * 
from .forms import *
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import io
from reportlab.lib import colors

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
    return render(request,"edit.html",{'trainee':trainee})
    
       
def updateTrainee(request,id):
      trainee = Trainee.objects.get(TraineeId = id)           
      form = TraineeForm(request.POST , instance = trainee)
      if form.is_valid():
            form.save()
            return redirect("/")
      return render(request,"edit.html",{'trainee':trainee})
    


# myapp/views.py-----normal---- PDF 


# def export_to_pdf(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="data.pdf"'

#     buffer = io.BytesIO()
#     p = canvas.Canvas(buffer, pagesize=letter)
    
#     data = Trainee.objects.all().values('Name', 'ContactNo','ContactAddress','EmailAddress','BatchNo')
    
#     y = 750
#     for item in data:
#         p.drawString(100, y, f"{item['Name']} - {item['ContactNo']} -  {item['ContactAddress']} - {item['EmailAddress']} - {item['BatchNo']}")
#         y -= 20

#     p.showPage()
#     p.save()
    
#     pdf = buffer.getvalue()
#     buffer.close()
#     response.write(pdf)
    
#     return response

def export_to_excel(request):
    data = Trainee.objects.all().values('Name', 'ContactNo','ContactAddress','EmailAddress','BatchNo')
    df = pd.DataFrame(list(data))

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
    
    df.to_excel(response, index=False)
    
    return response
        

# myapp/views.py------table wise---PDF


def export_to_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="data.pdf"'

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    data = Trainee.objects.all().values('Name', 'ContactNo','ContactAddress','EmailAddress','BatchNo')
    data_list = list(data)
    
    if not data_list:
        p.drawString(100, 700, "No data available.")
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    
    
    # Set table position
    x = 50
    y = 700
    row_height = 20
    col_width = [150, 100, 200, 100, 100]  # Define column widths for each column
    
    p.setFont("Helvetica-Bold", 12)
    headers = ["Name", "ContactNo", "ContactAddress", "EmailAddress", "BatchNo"]
    for i, header in enumerate(headers):
        p.drawString(x + sum(col_width[:i]), y, header)
    y -= row_height

    # # Draw table header
    # p.setFont("Helvetica-Bold", 12)
    # p.drawString(x, y, "Name")
    # p.drawString(x + col_width[0], y, "ContactNo")
    # p.drawString(x + col_width[0] + col_width[1], y, "ContactAddress")
    # p.drawString(x + col_width[0] + col_width[1] + col_width[2], y, "EmailAddress")
    # p.drawString(x + col_width[0] + col_width[1] + col_width[2] + col_width[3], y, "BatchNo")
     
    # y -= row_height

    # Draw header border
    p.setStrokeColor(colors.black)
    p.line(x, y + row_height, x + sum(col_width), y + row_height)

    # Reset font for data rows
    p.setFont("Helvetica", 12)

    for item in data:
        p.drawString(x, y, item['Name'])
        p.drawString(x + col_width[0], y, str(item['ContactNo']))
        p.drawString(x + col_width[0] + col_width[1], y, item['ContactAddress'])
        p.drawString(x + col_width[0] + col_width[1] + col_width[2], y,(item['EmailAddress']))
        p.drawString(x + col_width[0] + col_width[1] + col_width[2] + col_width[3], y, str(item['BatchNo']))
        
        y -= row_height

        # Draw row border
        p.line(x, y + row_height, x + sum(col_width), y + row_height)

    # Draw bottom border
    p.line(x, y + row_height, x + sum(col_width), y + row_height)

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
        