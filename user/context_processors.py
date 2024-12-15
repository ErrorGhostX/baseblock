from django.contrib.auth.decorators import login_required
from django.conf import settings

def user_profile(request):
    """
    Контекстный процессор для передачи профиля текущего пользователя в шаблон.
    """
    if request.user.is_authenticated:
        try:
            profile = request.profile # Предполагается, что есть связь OneToOneField с моделью Profile
            return {'profile': profile}
        except AttributeError:
            pass
    return {'profile': None}
