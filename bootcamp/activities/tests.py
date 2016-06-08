from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.core.urlresolvers import reverse


from bootcamp.activities.models import Activity, Notification
from bootcamp.activities.views import notifications, last_notifications, check_notifications

class ActivityModelTest(TestCase):
    
    def setUp(self):
        # creates a fictif user
        u = User()
        u.username = "testusername"
        u.password = "secretpassword"
        u.save()
        
        # create an activity related to that user
        activity = Activity()
        activity.user = u
        activity.activity_type = "Favorite"
        activity.date = timezone.now()
        
        # check we can save it to the database
        activity.save()
        
        # creates two fictif users
        u1 = User()
        u1.username = "testusername1"
        u1.password = "secretpassword1"
        u1.save()
        u2 = User()
        u2.username = "testusername2"
        u2.password = "secretpassword2"
        u2.save()
        
        # create one notification for each type of notification
        # Liked
        notifL = Notification()
        notifL.from_user = u1
        notifL.to_user = u2
        notifL.date = timezone.now()
        notifL.notification_type = 'Liked' # this is a like
        # save it to the database
        notifL.save()
        # Commented
        notifC = Notification()
        notifC.from_user = u1
        notifC.to_user = u2
        notifC.date = timezone.now()
        notifC.notification_type = 'Commented'
        # save it to the database
        notifC.save()
        # Favorited
        notifF = Notification()
        notifF.from_user = u1
        notifF.to_user = u2
        notifF.date = timezone.now()
        notifF.notification_type = 'Favorited'
        # save it to the database
        notifF.save()
        # Answered
        notifA = Notification()
        notifA.from_user = u1
        notifA.to_user = u2
        notifA.date = timezone.now()
        notifA.notification_type = 'Answered'
        # save it to the database
        notifA.save()
        # Accepted answer
        notifW = Notification()
        notifW.from_user = u1
        notifW.to_user = u2
        notifW.date = timezone.now()
        notifW.notification_type = 'Accepted Answer'
        # save it to the database
        notifW.save()
        # Edited article
        notifE = Notification()
        notifE.from_user = u1
        notifE.to_user = u2
        notifE.date = timezone.now()
        notifE.notification_type = 'Edited Article'
        # save it to the database
        notifE.save()
        # Also commented
        notifS = Notification()
        notifS.from_user = u1
        notifS.to_user = u2
        notifS.date = timezone.now()
        notifS.notification_type = 'Also Commented'
        # save it to the database
        notifS.save()
    
    def test_retrieve_activity(self):
        
        # check if we can retrieve it from the database
        activity_in_database = Activity.objects.all()
        self.assertEquals(len(activity_in_database), 1)
        only_activity_in_db = activity_in_database[0]
        self.assertEquals(only_activity_in_db.activity_type, 'Favorite')
        
        # check it return well its unicode
        self.assertEqual(only_activity_in_db.__unicode__(),'Favorite')
        
        
    def test_retrieve_notifications(self):
        
        # check we can retrieve it from db
        notif_in_db = Notification.objects.all()
        self.assertEquals(len(notif_in_db), 7)
        for i in notif_in_db:
            print i.notification_type
        print notif_in_db
        notifS_in_db = notif_in_db[0]
        self.assertEquals(notifS_in_db.notification_type, 'Also Commented') 
        #TODO check if the unicode is well rendered, which is not the case with the above set up, like "Liked" has to be saved as "L" or something
        
        
class ActivityViewTest(TestCase):
    
    def setUp(self):
        # every test need access to factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username = 'jacob', email='jacob@...', password='top_secret')
        
    def test_notifications_detail(self):
        # Create an instance of a GET request.
        request = self.factory.get('/notifications/')
        
        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user
        
        # Test the view
        response = notifications(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Notifications', response.content)
    
    """
    def test_notifications_appear_to_the_user(self):
        # creates two fictif users
        u1 = User()
        u1.username = "testusername1"
        u1.password = "secretpassword1"
        u1.save()
        u2 = User()
        u2.username = "testusername2"
        u2.password = "secretpassword2"
        u2.save()
        
        # create one notification
        notifL = Notification()
        notifL.from_user = u1
        notifL.to_user = u2
        notifL.date = timezone.now()
        notifL.notification_type = 'Liked'
        
        # get the url and response of the view
        url = reverse(notifications, args=[u1])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(notifL.notification_type, response.content)
    """
