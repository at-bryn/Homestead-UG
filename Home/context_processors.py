from django.contrib.auth.models import Group

def is_agent(request):
    if request.user.is_authenticated:
        return {'is_agent': request.user.groups.filter(name="Agents").exists()}
    return {'is_agent': False}