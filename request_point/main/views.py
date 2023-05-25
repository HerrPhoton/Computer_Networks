from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import URLForm
from .models import URL
#import html_parser


# Create your views here.
def index(request):

    if request.method == 'POST':
        form = URLForm(request.POST)

        if form.is_valid():
            form.save()
            redirect('success')
            #df = html_parser.parser(form)
            
        #df.to_csv(r'./table/zarina.csv', index = 0)
        #render(request, 'main/index.html', {"df": df})

    form = URLForm()
    return render(request, 'main/index.html', {"form": form})


def success(request):

    url = URL.objects.all()
    return HttpResponse(f'<h4>{str(url)}</h4>')
