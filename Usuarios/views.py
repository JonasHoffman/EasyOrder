from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def login_usuario(request):

    if request.user.is_authenticated:
        return redirect("interface:minhaloja")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:

            login(request, usuario)

            perfil = getattr(usuario, "perfil", None)

            if perfil and perfil.loja:
                return redirect("interface:minhaloja")

            return redirect("interface:home")

        messages.error(
            request,
            "Usuário ou senha inválidos."
        )

    return render(
        request,
        "login.html"
    )