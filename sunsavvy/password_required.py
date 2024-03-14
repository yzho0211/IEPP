from functools import wraps
from django.shortcuts import render

def password_required(password):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.method == 'POST':
                entered_password = request.POST.get('password')
                if entered_password == password:
                    return view_func(request, *args, **kwargs)
                else:
                    # 如果密码错误，返回带有密码表单和错误消息的页面
                    return render(request, 'password.html', {'error_message': 'Incorrect password. Please try again.'})
            else:
                # 如果是 GET 请求，返回密码输入页面
                return render(request, 'password.html', {'error_message': None})
        return _wrapped_view
    return decorator
