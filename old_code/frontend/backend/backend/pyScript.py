from django.shortcuts import render

def standby(request):
    return render(request, 'index.html')

def alert(request):
    return render(request, 'index.html', {'alert':'Processing your request...'})
