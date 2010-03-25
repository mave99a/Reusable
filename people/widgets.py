from models import User

def alltop(request, num=5):
    return User.all().fetch(num)

def weeklytop(request, num=5):
    return User.all().fetch(num)

def following(request):
    return User.all().fetch(10)

def followedby(request):
    return User.all().fetch(10)
