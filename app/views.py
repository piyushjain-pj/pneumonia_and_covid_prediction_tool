import app.pneumonia as pn
import app.covid_19 as cd
import core.settings as settings
import random
import string
import mysql.connector
import os
from django.shortcuts import render
from . import pool
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import loader
from django.http import HttpResponse
from django import template
from django.core.mail import send_mail
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Media_ROOT = os.path.join(root, 'media')
images = os.listdir(Media_ROOT)
imgpath = os.path.join(Media_ROOT, "")

# # add this code in function:
# ctx = {
#     'subject': "subjectin",
#     'userMsg': "messagein",
# }
# heading = "Your heading"
# messageContent = get_template('yourTemplate.html').render(ctx)  # sending value on HTML page through context
# msg = EmailMessage(heading, messageContent, settings.EMAIL_HOST_USER,['jpiyush410@gmail.com'])
# msg.content_subtype = 'html'
# msg.send()


@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'home.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template  = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))
        
def webindex(request):
    context = {}
    html_template = loader.get_template('website/index.html')
    return HttpResponse(html_template.render(context, request))

def homepage(request):
    context = {}
    html_template = loader.get_template('website/index2.html')
    return HttpResponse(html_template.render(context, request))

def patientreg(request):

    # if this is a POST request we need to process the form data
    context = {}
    html_template = loader.get_template('website/patient-registration.html')
    try:
        if request.method == 'POST':

            if request.POST['regtype'] == "pneumonia":
                context['RegistrationType'] = "Pneumonia"
            else:
                context['RegistrationType'] = "Covid-19"

            return HttpResponse(html_template.render(context, request))
        else:
            return HttpResponse(html_template.render(context, request))


    except Exception as e:
        print(e)

# def setXrayImgPath(imgdir):
#     result = cd.get_input_userdata(imgdir)
#     class_label = []
#     if result == 0:
#         class_label.append("Pneumonia")
#         output = "Predicted Class is[0]\nReport Positive Pneumonia Case Found"
#         print("Predicted Class is", result, "\n", class_label, "Detect")
#     else:
#         class_label.append("Normal")
#         output = "Predicted Class is [1]\nReport Negative\nNormal lungs Found"
#         print("Predicted Class is", result, "\n",
#               class_label, "\nReport Negative")

def predictions(request):


    insert_query = """
    INSERT INTO patient_registration (first_name, middle_name, last_name, dob, gender, blood_group, occupation, phone, email, address, city, zip, regtype, image, result, predictedclass) VALUES (%s,%s,%s,date(%s),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """


    prediction = ""
    value_tuple= list()
    mydb, mycursor = pool.connection()
    print(mydb.is_connected())
    icon = request.FILES['image']

    # printing lowercase
    letters = string.ascii_lowercase
    letters = "".join(random.choice(letters) for i in range(10))
    imgpath = os.path.join(Media_ROOT, letters+icon.name)
    F = open(imgpath, "wb")
    for chunk in icon.chunks():
        F.write(chunk)
    F.close()
    print(imgpath)

    if request.POST['regtype'] == "Pneumonia":
        prediction = pn.get_input_userdata(imgpath)
        if prediction == 0:
            output = "Predicted Class is [0] Report Positive Pneumonia Case Found"
            print("Predicted Class is", prediction[0],"Pneumonia Detect In lungs")
        else:
            output = "Predicted Class is [1] Report Negative Normal lungs Found"
            print("Predicted Class is ",prediction[0]," Report Negative")
    else:
        prediction = cd.get_input_userdata(imgpath)
        if prediction == 0:
            output = "Predicted Class is[0] Report Positive Covid-19 Case Found"
            print("Predicted Class is", prediction[0],"Pneumonia Detect In lungs")
        else:
            output = "Predicted Class is [1] Report Negative Normal lungs Found"
            print("Predicted Class is ",prediction[0]," Report Negative")
    

    result = output


    if request.method == "POST":
        value_tuple.append(request.POST['first_name'])
        value_tuple.append(request.POST['middle_name'])
        value_tuple.append(request.POST['last_name'])
        value_tuple.append(request.POST['dob'])
        value_tuple.append(request.POST['gender'])
        value_tuple.append(request.POST['blood_group'])
        value_tuple.append(request.POST['occupation'])
        value_tuple.append(request.POST['phone'])
        value_tuple.append(request.POST['email'])
        value_tuple.append(request.POST['address'])
        value_tuple.append(request.POST['city'])
        value_tuple.append(request.POST['zip'])
        value_tuple.append(request.POST['regtype'])
        value_tuple.append(letters+icon.name)
        value_tuple.append(result)
        value_tuple.append(int(prediction[0]))





    mycursor = mydb.cursor()
    mycursor.execute(insert_query, tuple(value_tuple))
    lastrowid = mycursor.lastrowid
    mydb.commit()
    mydb.close()

    fullname = request.POST['first_name']+" "+request.POST['last_name']

    returndata = """
        <strong>Hello Dear,</strong>
        <h4>Test Name : {3} </h4>
        <table class="table">
            <thead>
                <tr>
                    <th>Pateint Name</th>
                    <th>Dob ( Gender )</th>
                    <th>Blood Group</th>
                    <th>Result Result</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td scope="row">{0}</td>
                    <td>{1}  ( {4} )</td>
                    <td>{5}</td>
                    <td>{2}</td>
                </tr>
            </tbody>
        </table>
    """.format(fullname, request.POST['dob'], result, request.POST['regtype'], request.POST['gender'], request.POST['blood_group'])



    subject = "Your "+  request.POST['regtype'] + "Diagnosis Report"
    html_content = returndata
    email = EmailMessage(subject, html_content,"cnpptool@gmail.com", [request.POST['email']])
    email.content_subtype = "html"
    res = email.send()
    
    from django.contrib import messages
    messages.success(request, returndata, extra_tags='report')
    messages.success(request, 'The Report has been sent to your {0} email address '.format(
        request.POST['email']), extra_tags='msg')
    

    return redirect("/")


def pneumonia_reporting(request):
    mydb, mycursor = pool.connection()
    print(mydb.is_connected())

    mycursor.execute("SELECT * FROM djangonew.patient_registration where regtype = 'Pneumonia'")
    records = mycursor.fetchall()
    print(records)
    html_template = loader.get_template('pneumonia_reporting.html')
    return HttpResponse(html_template.render({'records': records}, request))


def covid_reporting(request):
    mydb, mycursor = pool.connection()
    print(mydb.is_connected())

    mycursor.execute("SELECT * FROM djangonew.patient_registration where regtype = 'Covid-19'")
    records = mycursor.fetchall()
    print(records)

    # html_template = loader.get_template('covid_reporting.html')
    return render(request, "covid_reporting.html", {"records": records})
