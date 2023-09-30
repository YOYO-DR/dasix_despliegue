# patron correo
from django.core.validators import validate_email


from django.contrib.auth.password_validation import validate_password
from django.forms import ValidationError

import ast

def validar_patron_correo(email):
    try:
        validate_email(email)
        return True
    except:
        return False

def validar_contra(contra, usuario=None):
    try:
        validate_password(contra, usuario)
        return [True]
    except ValidationError as e:
        errors = e.error_list
        errores = []
        for error in errors:
            # como retorna algo como "['error']", con ast analizo el string, y lo convierto a lista y luego accedo a su valor 0
            error=ast.literal_eval(str(error))[0]
            errores.append(error)
        return [False, errores]
