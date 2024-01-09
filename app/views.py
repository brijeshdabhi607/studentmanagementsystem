from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from app.models import CustomUser, Categories, Course, Level


# Create your views here.
def home(request):
    categoryobj = Categories.objects.all().order_by("id")[0:5]
    courseobj = Course.objects.all().order_by("id")[0:5]
    return render(request, 'Main/homepage.html', {'category': categoryobj, 'course': courseobj})


def base(request):
    return render(request, 'base.html')


def single_course(request):
    category = Categories.objects.all().order_by("id")
    level = Level.objects.all().order_by("id")
    course = Course.objects.all().order_by("id")
    context = {
        "category": category,
        "level": level,
        "course": course,
    }
    return render(request, "Main/single_course_page.html", context)


def contact(request):
    return render(request, "Main/contact_us.html")


def about(request):
    return render(request, "Main/about_us.html")


def register(request):
    if request.method == "POST":
        username= request.POST.get('username')
        email= request.POST.get('email')
        password= make_password(request.POST.get('password'))
        user = CustomUser.objects.create(username=username, email=email, password=password)
        return redirect("/")
    return render(request, "registration/register.html")


def do_login(request):
    if request.method == "POST":
        # username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user= authenticate(request, username=email, password=password)
        print("User is ", user)
        print(email,"     ", password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials")
            return redirect("login")
    else:
        return redirect("login")


def profile(request):
    return render(request, "registration/profile.html")


def update_profile(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = CustomUser.objects.get(email=email)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request, "Profile Updated Successfully")
        return redirect("profile")


def filter_data(request):
    categories = request.GET.getlist('category[]')
    price = request.GET.getlist('price[]')
    if price == ["PriceFree"]:
        course = Course.objects.filter(price = 0)
    elif price == ["PricePaid"]:
        course = Course.objects.filter(price__gt = 0)
    elif price == ["PriceAll"]:
        course = Course.objects.all()
    elif categories:
        course = Course.objects.filter(category__id__in=categories)
    else:
        course = Course.objects.all().order_by('id')
    t = render_to_string("ajax/course.html", {"course": course})
    return JsonResponse({'data': t})

def search_course(request):
    query = request.GET.get("query")
    print(query)
    course = Course.objects.filter(title__icontains = query)
    print(course)
    context = {
        "course": course,
    }
    return render(request, "search/search.html", context)