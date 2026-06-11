# Context processors generales para todos los templates

def navbar_menu(request):
    menu_items = [
        {'name': 'Inicio', 'url': 'index', 'login_required': 'false'},
        {'name': 'Prode', 'url': 'prode', 'login_required': 'true'},
        {'name': 'Clasificación', 'url': 'clasificacion', 'login_required': 'false'}
    ]
    return {'menu_items': menu_items}