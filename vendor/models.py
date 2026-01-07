from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification
from datetime import date, datetime, time

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    # Add slug field in Vendor Model.Sluging vendor_name/Restaurant name 
    # is required to show the list of food item for a particular vendor from marketplace view
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license') # it goes to media folder
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    
    # Create a member function to check whther the vendor is open or not
    # this is_open function will exactly work as vendor model database field

    def is_open(self):
        # Check opening hour for current day
        to_day = date.today()
        today= to_day.isoweekday()
        current_opening_hours = OpeningHour.objects.filter(vendor=self, day=today)

        # Current Time to check whether the vandor is open or closed
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')

        is_open = None
        for i in current_opening_hours:
            if not i.is_closed:
                start = str(datetime.strptime(i.from_hour, '%I:%M %p').time())
                end = str(datetime.strptime(i.to_hour, '%I:%M %p').time())
                # print(start, end)
                if current_time > start and current_time < end :
                    is_open = True
                    break # break is used here if the vendor have multiple time in a day but open for anyone then exit from if condition
                else:
                    is_open = False
        return is_open
    
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
    
DAYS = [
    (1, ('MONDAY')),
    (2, ('TUESDAY')),
    (3, ('WEDNESDAY')),
    (4, ('THURSDAY')),
    (5, ('FRIDAY')),
    (6, ('SATURDAY')),
    (7, ('SUNDAY')),
]
    
HOUR_DAY_24 = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in (0, 30)] # List Comprehension

class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_DAY_24, max_length=10, blank=True)
    to_hour = models.CharField(choices=HOUR_DAY_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', '-from_hour') # add - here to show the time in asending order
        unique_together = ('vendor', 'day', 'from_hour','to_hour')

    def __str__(self):
        # It is django in-build function to show string representation of day, where day is the day field name in the model
        # This method will show the label/Name of the day instead of interger representation
        return self.get_day_display() 