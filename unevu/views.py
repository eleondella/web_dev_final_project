from django.shortcuts import render,redirect
from django.template import loader
from django.contrib.auth import authenticate,login,logout, get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import json
from django.http import Http404
from unevu.forms import UserForm

from unevu.models import *

def home(request):    
    context_dict = {}
    context_dict['universities'] = University.objects.all()
    context_dict['top_unis'] = University.objects.order_by('-avgRating')[:5]
    context_dict['top_courses'] = Course.objects.order_by('-avgRating')[:5]
    response = render(request, 'unevu/home.html', context=context_dict)
    
    return response

def about(request):
    context_dict = {}
    
    response = render(request, 'unevu/about.html', context=context_dict)
    
    return response

def register(request):
    registered = False
    
    if ('submit' in request.POST):
        form = UserForm(data=request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            user.set_password(password)
            user.save()
            
            registered = True
            
            if registered:
                u = User.objects.get(username=username)
                UserProfile.objects.create(user_id=u.id)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('/')     
        else:
            print(form.errors)
    else:
        form = UserForm()
        
    return render(request,
                  'unevu/register.html',
                  {'form': form,
                   'registered': registered
                  })


def user_login(request):
    if request.method == 'POST':
        if 'home' in request.POST:
           return HttpResponseRedirect('/')
        elif 'submit' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
    
            user = authenticate(username=username, password=password)
            if user is None:
                User = get_user_model()
                user_queryset = User.objects.all().filter(email__iexact=username)
                if user_queryset:
                    username = user_queryset[0].username
                    user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.POST.get('remember_me'):
                        request.session.set_expiry(settings.KEEP_LOGGED_DURATION)
                    
                    #Once logged in go back to home page    
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponse("Your Unevu account is disabled.")
            else:
                print("Invalid login details: {0}, {1}".format(username, password))
                return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'unevu/login.html', {})

def user_logout(request):
    logout(request)

    return redirect('/')

def choose_uni(request):
    context_dict = {}
    response = render(request, 'unevu/home.html', context=context_dict)
    return response
    
def uni_details(request):
    if request.method == "POST":
        if request.POST.get("what")=="query-schools":
            name = request.POST.get('university')
            university = University.objects.get(name=name)
            json_university = json.dumps({"id" : university.id})
            return HttpResponse(json_university, content_type ="application/json")

def university(request,uni_id):
    if request.method == "GET":
        university = University.objects.get(id=uni_id)
        schools = [school.name for school in School.objects.filter(university_id=university.id)]
        rating = None
        uni_desc = university.description
        uni_reviews = UniReview.objects.filter(university=university)
        try:
            rating = sum([int(review.rating) for review in uni_reviews])/len(uni_reviews)
        except:
            pass
        print(rating)

        context_dict = {"schools":schools,"university":university,"rating":rating}
        response = render(request, 'unevu/university.html', context=context_dict)
        return response

def school_details(request):
    if request.method == "POST":
        if request.POST.get("what")=="query-subjects":
            id = int(request.POST.get('university'))
            school_name = request.POST.get('school')
            university = University.objects.get(id=id)
            school = School.objects.get(university_id=university.id,name=school_name)
            courses = [course.name for course in Course.objects.filter(school_id=school.id)]
            json_courses = json.dumps({"courses" : courses})
            return HttpResponse(json_courses, content_type ="application/json")
        elif request.POST.get("what")=="course-selected":
            id = int(request.POST.get('university'))
            school_name = request.POST.get('school')
            course_name = request.POST.get('course')
            university = University.objects.get(id=id)
            school = School.objects.get(university_id=university.id,name=school_name)
            course = Course.objects.get(school_id=school.id,name=course_name)
            json_selected_course = json.dumps({"id" : course.id})
            return HttpResponse(json_selected_course, content_type ="application/json")

    return Http404("Course not found or access denied. Please go back.")


def review_course(request,course_id):
    course = Course.objects.get(id=course_id)
    teachers = [teacher.name for teacher in Teacher.objects.filter(school_id= course.school_id)]
    reviews = CourseReview.objects.filter(course=course)
    context_dict = {"title":course.name.title(),"description":course.description,"teachers":teachers,
                    "reviews":reviews, "uni_name":course.school.university.name}
    return render(request, 'unevu/subjects_review.html', context=context_dict)

def add_review(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            what = request.POST.get('what')
            if what == "course":
                course_id = request.POST.get('course')
                review = request.POST.get('review')
                rating = request.POST.get('rating')
                course = Course.objects.get(id=int(course_id))
                course.avgRating  = (course.avgRating * course.noOfRatings + int(rating))/(course.noOfRatings+1)
                course.noOfRatings = course.noOfRatings+1
                course.save()
                course_review = CourseReview.objects.create(course=course,username=request.user,reviewText=review,rating=rating)
                course_review.save()
                return 
    else:
        return HttpResponse("Error")
