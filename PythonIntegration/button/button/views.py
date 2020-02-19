from django.shortcuts import render

def button(reqeust):
    return render(reqeust, 'home.html')

def output(request):
    print("Success!")
    str = "Success!"
    return render(request, 'home.html', {'data':str})
