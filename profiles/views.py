from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect,ensure_csrf_cookie
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import UpdatePersonalInformationForm, UpdateAddressInformationForm, UpdateProfileInformationForm, ImageUploadForm

from django.contrib.auth.models import User
from authenticate.data_validator import ValidateIdNumber
from .models import Profile, PersonalInformation, AddressInformation, ProfileImage
from django.db.utils import IntegrityError
from PIL import Image as PilImage
import os
import re
from authenticate.data_validator import ValidateIdNumber
# Create your views here.

@ensure_csrf_cookie
def render_profile_page(request):
    if request.user.is_authenticated:
        return render(request,'user_profile.html')
    else:
        return redirect('render_auth_page')


@csrf_protect
def update_user_profile(request):
    if request.user.is_authenticated:

        pr = Profile.objects.all()
        if request.method == 'POST':
            try:
                json_data = json.loads(request.body)
            except Exception :
                return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
            print(json_data)
            data = {
                'username' : json_data.get('username'),
                'first_name' : json_data.get('first_name'),
                'last_name' : json_data.get('last_name'),
                'email' : json_data.get('email'),
                'phone' : json_data.get('phone'),
                'idnumber': json_data.get('idnumber'),
                'r_username' : f'{request.user.username}',
                'r_email' : f'{request.user.email}',
                'r_phone' : 'False'
                # 'r_idnum' : f'{request.user.profile.idnumber}'
            }
       
            for key, value in data.items():
                if key == None or value == None:
                    return JsonResponse({'errors': f'{key} field is required ', 'status':'error'}, status=404)
            form = UpdateProfileInformationForm(data)
            if form.is_valid() : 
                exist = User.objects.filter(email=data['email']).exists()
                if exist:
                    user = User.objects.get(email=data['email'])
                    if user.email == request.user.email:
                        pass
                    else:
                        raise forms.ValidationError(f"Email: {email} is already taken")

                exist = User.objects.filter(username=data['username']).exists()
                if exist:
                    user = User.objects.get(username=data['username'])
                    if user.username == request.user.username:
                        pass
                    else:
                        raise forms.ValidationError(f"Username:{username} is already taken")
                try :
                    user = User.objects.get(id=request.user.id)
                    print(user)
                    user.username = data['username']
                    user.first_name = data['first_name']
                    user.last_name = data['last_name']
                    user.email = data['email']
                    # user.password = data['password']
                   
                    user.profile.idnumber = data['idnumber']
                    user.profile.phone = data['phone']
                    user.profile.age = ValidateIdNumber(data['idnumber']).get_age()
                    user.profile.gender = ValidateIdNumber(data['idnumber']).get_gender()
                    user.profile.save()
                    user.save()
                    print("======================")
                    print(user.profile.phone)
                    return JsonResponse({'message':f'User profile for {user.username} is updated successfuly', 'status':'success'}, status=201) 
                except Exception as e:
                    return JsonResponse({'errors': f'{e}', 'status':'error'}, status=404)
            else:
                return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
        else:
            return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    else:       
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)


@csrf_protect
def update_personal_info(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                json_data = json.loads(request.body)
            except Exception :
                return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
            personal_data = {
                'linkedin_profile' : json_data.get('linkedin_profile'),
                'personal_website' : json_data.get('personal_website'),
                'job_title'  : json_data.get('job_title'),
                'current_employer' : json_data.get('current_employer'),
                'years_of_expreince' : json_data.get('years_of_expreince'),
                'industry' : json_data.get('industry'),
                'carear_level' : json_data.get('carear_level'),
                'desired_job' : json_data.get('desired_job'),
                'job_location' : json_data.get('job_location')
                }
            personal_data_form =  UpdatePersonalInformationForm(personal_data)
            if personal_data_form.is_valid() : #and address_data_form.is_valid():
                try:
                    # address_data_form = AddressInformationForm(address_data)
                    personal_info = PersonalInformation.objects.create(user=request.user, linkedin_profile=personal_data['linkedin_profile'],personal_website=personal_data['personal_website'],job_title=personal_data['job_title'], current_employer=personal_data['current_employer'], years_of_expreince=personal_data['years_of_expreince'], industry=personal_data['industry'], carear_level=personal_data['carear_level'], desired_job=personal_data['desired_job'], job_location=personal_data['job_location'] )
                    # address_info = AddressInformation.objects.create(user=request.user, street_address_line=address_data['street_address_line'], street_address_line1=address_data['street_address_line1'], city=address_data['city'], province=address_data['province'], postal_code=address_data['postal_code'] )
                    personal_info.save()
                    # address_info.save()     
                    return JsonResponse({"message":"update personal information success"})
                except IntegrityError:
                    personal_information = PersonalInformation.objects.get(user_id=request.user.id)
                    print(personal_information)
                    personal_information.linkedin_profile = personal_data['linkedin_profile']
                    personal_information.personal_website = personal_data['personal_website']
                    personal_information.job_title = personal_data['job_title']
                    personal_information.current_employer = personal_data['current_employer']
                    personal_information.years_of_expreince = personal_data['years_of_expreince']
                    personal_information.industry = personal_data['industry']
                    personal_information.carear_level = personal_data['carear_level']
                    personal_information.desired_job = personal_data['desired_job']
                    personal_information.job_location = personal_data['job_location']
                    personal_information.save()
                    print('=========done=========')
                    return JsonResponse({"message":"update personal information success", "status":"success"}, status=200)
                except Exception as e: 
                    return JsonResponse({'errors':f'{e}', 'status':'error'}, status=404)
            else:
               return JsonResponse({"errors":personal_data_form.errors, "status":"error"}, status=400) 
        else:
            return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    else:       
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)



@csrf_protect
def update_address_info(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                json_data = json.loads(request.body)
            except Exception :
                return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
            address_data = {
                'street_address_line' : json_data.get('street_address_line'),
                'street_address_line1' : json_data.get('street_address_line1'),
                'city'  : json_data.get('city'),
                'province' : json_data.get('province'),
                'postal_code' : json_data.get('postal_code')
                
                }
            
            address_data_form =  UpdateAddressInformationForm(address_data)
            if address_data_form.is_valid() : #and address_data_form.is_valid():
                try:
            
                    address_info = AddressInformation.objects.create(user=request.user, street_address_line=address_data['street_address_line'], street_address_line1=address_data['street_address_line1'], city=address_data['city'], province=address_data['province'], postal_code=address_data['postal_code'] )
                    address_info.save()     
                    return JsonResponse({"message":"update personal information success"})
                except IntegrityError:
                    address_information = AddressInformation.objects.get(user_id=request.user.id)
                    print(address_information)
                    address_information.street_address_line = address_data['street_address_line']
                    address_information.street_address_line1 = address_data['street_address_line1']
                    address_information.city = address_data['city']
                    address_information.province = address_data['province']
                    address_information.postal_code = address_data['postal_code']
                   
                    address_information.save()
                    print('=========done=========')
                    return JsonResponse({"message":"update personal information success", "status":"success"}, status=200)
                except Exception as e: 
                    return JsonResponse({'errors':f'{e}', 'status':'error'}, status=404)
            else:
               return JsonResponse({"errors":address_data_form.errors, "status":"error"}, status=400) 
        else:
            return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    else:       
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@csrf_protect
def upload_profile_image(request):
    if request.method == 'POST':

        try:
            image = request.FILES['image']
            # return JsonResponse({'errors': {'file' :['Bad Request']}, 'status': 'error'}, status=400)
        except Exception as e:
            return JsonResponse({'errors': f'{e}', 'status': 'error'}, status=400)
        try:
            if not image or image.name == '':
                return JsonResponse({'errors':'No selected file', 'status': 'error'}, status=400)
            if not image and not allowed_file(image.filename):
                return JsonResponse({'errors':'File type not allowed', 'status': 'error'}, status=400)
            img = PilImage.open(image)
            img.verify()  # Verify that this is a valid image
            # If user does not select a file, the browser submits an empty file without a filename
            try:
                profile_image = ProfileImage.objects.create(user=request.user,image=image) 
                profile_image.save()
                return JsonResponse({'message': 'Image uploaded successfully', 'status': 'success'}, status=201)
            except:
                user_profile_image = ProfileImage.objects.get(user=request.user)

                if user_profile_image:
                    ext= user_profile_image.image.path.split('/')[-1].split('_')[-1].split('.')[-1]
                    name = user_profile_image.image.path.split('/')[-1].split('_')[0:-1]
                    if type(name) is type(list('jeff')):
                        name = '_'.join(name)
                    filename = name+'.'+ext
                    files = user_profile_image.image.path.split('/')
                    files[-1] = filename
                    file_to_delete = '/'.join(files)
                    print(file_to_delete)
                    if os.path.isfile(file_to_delete):
                        os.remove(file_to_delete)

                    user_profile_image.image.delete()
                    user_profile_image.image = image
                    user_profile_image.save()
                    return JsonResponse({'message': 'Image uploaded successfully', 'status': 'success'}, status=201)
                else:
                    return JsonResponse({'errors': 'NOT FOUND', 'status': 'error'}, status=400)

        except (IOError, SyntaxError):
            return JsonResponse({'errors': 'Invalid image file', 'status': 'error'}, status=400)
        else:
            return JsonResponse({'errors': form.errors, 'status': 'error'}, status=400)
    return JsonResponse({'errors': 'Invalid request method', 'status': 'error'}, status=400)

#==================================================================================================================================

