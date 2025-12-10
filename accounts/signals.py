from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import User, UserProfile

# Django signal
# Signals are refer to utility or feature that helps to connect the events with actions
# Here sender is User
# This is the example of POST_SAVE signal
@receiver(post_save, sender=User) # this is a decorator name receiver, which use to connect receiver with sender
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    # as soon as the user is created, the created feild will become true and profile will be created
    print(created)
    if created:
       # print('Created the user profile')
       UserProfile.objects.create(user=instance)
       print('User profile is created')
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print('Profile is updated')
        except:
            # Create the user profile if not exist
            UserProfile.objects.create(user=instance)
            print('Profile was not exists, created newly')
        #print('User profile is updated')

# Example of pre_save signal
@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(instance.username, 'This user is being saved')


#post_save.connect(post_save_create_profile_receiver, sender=User) # instead we can use decorator. 