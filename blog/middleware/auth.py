from django.db.backends.sqlite3.base import none_guard
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    def process_request(self,request):
        list = ['/edit/']
        if request.path_info not in list:
            return None

        info_dict = request.session.get('info')
        if info_dict:
            return
        else:
            return redirect('login')