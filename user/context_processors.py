from django.contrib.auth.decorators import login_required
from django.conf import settings

def user_profile(request):
    """
    Контекстный процессор для передачи профиля текущего пользователя в шаблон.
    """
    if request.user.is_authenticated:
        try:
            # Если пользователь аутентифицирован, передаем URL изображения профиля
            profile_image = request.user.profile_image.url
            return {'profile_image': profile_image}
        except AttributeError:
            # Если у пользователя нет profile_image
            return {'profile_image': settings.STATIC_URL + "default_avatar.png"}  # Указываем путь к изображению по умолчанию
    # Для анонимных пользователей
    return {'profile_image': settings.STATIC_URL + "default_avatar.png"}

