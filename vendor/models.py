from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='vendor/license') # it goes to media folder
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    
    # This save function will triggered whenever we actually press the save button
    # * args- arguments, **kwargs- Keyword arguments
    # These two arguments parameters will use whenenver we do not know how many paramet this fuction will have
    def save(self, *args, **kwargs):
        # Check whether it is update of this particualr vendor or not
        if self.pk is not None:
            # Update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                        'user': self.user,
                        'is_approved': self.is_approved,
                    }
                if self.is_approved == True:
                    # send email notification
                    mail_subject = "Contragulation! Your restaurant has been approved."
                    send_notification(mail_subject, mail_template, context)
                else:
                    # send email notification
                    mail_subject = "We're sorry! You are not eligible publishing your food menu on our marketplace"
                    send_notification(mail_subject, mail_template, context)
        # This super fuction is actually allow you to access save method of class Vendor
        return super(Vendor,self).save(*args, **kwargs)
