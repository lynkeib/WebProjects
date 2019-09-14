from django.shortcuts import render
from .forms import ContactsForm
from django.core.mail import EmailMessage


# Create your views here.
def contact(request):
    # form = ContactsForm(request.POST)
    form = ContactsForm()
    if request.method == "POST":
        form = ContactsForm(request.POST)
        if form.is_valid():

            con = form.save(commit=False)
            con.save()
            subject = "Thank you for the visiting!"
            message = "This is a confirmation email indicating that we received your " \
                      "message and will get back to you as soon as possible. Thank you!"
            email = EmailMessage(subject, message, to=[con.email])
            email.send()
            return render(request, 'contact.html', context={'form': ContactsForm()})
        else:
            return render(request, 'contact.html', context={'form': form})
    return render(request, 'contact.html', context={'form': form})
