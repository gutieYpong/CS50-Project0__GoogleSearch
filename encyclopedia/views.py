from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

from markdown2 import Markdown
from . import util
import os
import random

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class NewTaskForm(forms.Form):
    sub_input = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder":"Type in the subject title here."}))
    content_input = forms.CharField(label="", widget=forms.Textarea(attrs={"placeholder":"Type in the subject title here."}))

    def __init__(self, *args, **kwargs):

        super(NewTaskForm, self).__init__(*args, **kwargs)
        self.fields['sub_input'].initial = ""
        self.fields['content_input'].initial = ""


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def content(request, title):

    pages_list = util.list_entries()
    return_list = [page for page in pages_list if title.lower() == page.lower()]

    if len(return_list) == 0:

        title = "Oops! ERROR 404: requested page was not found."

        return render(request, "encyclopedia/page_error.html", {
                "title": "Oops! ERROR 404: requested page was not found.",
                })

    markdown = md2html(return_list[0])

    return render(request, "encyclopedia/page_content.html", {
        "title": title,
        "markdown": markdown
    })

    # return HttpResponseRedirect(reverse("encyclopedia:title", kwargs={'title': title}))


def search(request):

    if request.method == "POST":

        submit_value = request.POST.get('q')
        return_list = str_matching(submit_value)

        if len(return_list) == 1 and submit_value.lower() == return_list[0].lower():

            return HttpResponseRedirect('/wiki/'+return_list[0])

        else:

            return render(request, "encyclopedia/search_result.html", {
                "query": submit_value,
                "searchResults": return_list,
                "resultNum": len(return_list)
            })


def newpage(request):

    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewTaskForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the task from the 'cleaned' version of form data, get the data from submit form.
            sub = form.cleaned_data["sub_input"]
            paragraph = form.cleaned_data["content_input"]

            if sub.capitalize() not in util.list_entries():

                # Write the data into a new file.md
                f = open(os.path.join(BASE_PATH, 'entries', sub[:1].capitalize() + sub[1:] +'.md'), 'w+')
                f.write(paragraph)
                f.close()

                return HttpResponseRedirect(reverse("encyclopedia:index"))
            
            else:
                messages.error(request, "This thread has been created.")
                messages.error(request, "Please make a change.")

                return render(request, "encyclopedia/page_new.html", {
                    "form": form
                })
        else:
            return render(request, "encyclopedia/page_new.html", {
                "form": form
            })      

    return render(request, "encyclopedia/page_new.html", {
        "form": NewTaskForm()
    })

def editpage(request, subject):

    if request.method == "GET":
        
        form = NewTaskForm()

        f = open(os.path.join(BASE_PATH, 'entries', subject+'.md'), 'r')

        form.fields['sub_input'].initial = subject
        form.fields['content_input'].initial = f.read()

        return render(request, "encyclopedia/page_edit.html", {
            "form": form
        })

    else:
        
        form = NewTaskForm(request.POST)

        if form.is_valid():
            
            sub = form.cleaned_data["sub_input"]
            paragraph = form.cleaned_data["content_input"]

            # Write the data into a new file.md
            f = open(os.path.join(BASE_PATH, 'entries', sub +'.md'), 'w+')
            f.write(paragraph)
            f.close()

            return HttpResponseRedirect('/wiki/'+sub)


def randompage(request):

    pages_list = util.list_entries()
    ramdom_num = random.randint(0, len(pages_list) - 1)
    page_random = pages_list[ramdom_num]
   

    return HttpResponseRedirect('/wiki/'+page_random) # Redirect after POST


def str_matching(str1):

    pages_list = util.list_entries()
    return_list = [page for page in pages_list if str1.lower() in page.lower()]

    return return_list


def md2html(fname):

    markdowner = Markdown()

    f = open(os.path.join(BASE_PATH, 'entries', fname+'.md'), 'r')

    return markdowner.convert(f.read())
