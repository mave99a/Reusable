from user import get_current_user

class AuthMiddleware(object):
    def process_request(self, request):
        request.authuser = get_current_user(request)
        request.current_user = request.authuser.user