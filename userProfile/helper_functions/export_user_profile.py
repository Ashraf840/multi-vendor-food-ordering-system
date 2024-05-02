from userProfile.models import UserProfile



# [ It's a helper-func ]
# It's called in different view-funcs accross the project to grab particular user-profiles.
def export_user_profile(userID):
    u_id = userID
    u_profile = UserProfile.objects.get(id=u_id)
    return u_profile
