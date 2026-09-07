from django.shortcuts import render,redirect


def home(request):
    if request.user.is_authenticated:

        perfil = getattr(request.user, "perfil", None)

        if perfil and perfil.loja:
            return redirect("interface:minhaloja")

    return redirect("interface:homeinicial")
    

def homeDiagrama(request):
    return render(request, "templates/home.html")

def homeinicial(request):
    return render(request, "templates/homeinicial.html")