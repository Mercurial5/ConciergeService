from django.shortcuts import render


def chatPage(request, *args, **kwargs):
    return render(request, 'chatPage.html')
