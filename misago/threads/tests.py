from django.core.management import call_command
from django.utils import timezone, unittest
from django.test.client import RequestFactory
from misago.settings.models import Setting
from misago.forums.models import Forum
from misago.sessions.sessions import SessionMock
from misago.threads.models import Thread, Post, Change, Checkpoint
from misago.threads.testutils import create_thread, create_post 
from misago.users.models import User

class DeleteThreadTestCase(unittest.TestCase):
    def setUp(self):
        call_command('loaddata', quiet=True)
        self.factory = RequestFactory()
        
        Post.objects.all().delete()
        Thread.objects.all().delete()
        User.objects.all().delete()
        self.user = User.objects.create_user('Neddart', 'ned@test.com', 'pass')
        self.user_alt = User.objects.create_user('Robert', 'rob@test.com', 'pass')
        self.forum = Forum.objects.get(id=1)
        
        self.thread = create_thread(self.forum)
        self.post = create_post(self.thread, self.user)
        
    def test_deletion_owned(self):
        """Check if user content delete results in correct deletion of thread"""
        # Assert that test has been correctly initialised
        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(Post.objects.count(), 1)
        
        # Run test
        self.user.delete_content()
        self.assertEqual(Thread.objects.count(), 0)
        self.assertEqual(Post.objects.count(), 0)
        
    def test_deletion_other(self):
        """Check if user content delete results in correct deletion of post"""
        # Create second post
        self.post = create_post(self.thread, self.user_alt)
        
        # Assert that test has been correctly initialised
        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(Post.objects.count(), 2)
        
        # Run test
        self.user_alt.delete_content()
        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(Post.objects.count(), 1)
        
    def test_deletion_owned_other(self):
        """Check if user content delete results in correct deletion of thread and posts"""
        # Create second post
        self.post = create_post(self.thread, self.user_alt)
                
        # Assert that test has been correctly initialised
        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(Post.objects.count(), 2)
        
        # Run test
        self.user.delete_content()
        self.assertEqual(Thread.objects.count(), 0)
        self.assertEqual(Post.objects.count(), 0)
        
    def test_deletion_checkpoints(self):
        """Check if user content delete results in correct update of thread checkpoints"""
        # Create an instance of a GET request.
        request = self.factory.get('/customer/details')
        request.session = SessionMock()
        request.user = self.user_alt
        request.META['HTTP_USER_AGENT'] = 'TestAgent'
        
        # Create second and third post
        self.post = create_post(self.thread, self.user)
        self.post_sec = create_post(self.thread, self.user_alt)
        self.post_sec.set_checkpoint(request, 'locked')
        self.post_sec.save(force_update=True)
                
        # Assert that test has been correctly initialised
        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(Post.objects.count(), 3)
        
        # Run test
        self.user_alt.delete_content()
        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Checkpoint.objects.count(), 1)
        self.assertEqual(Post.objects.filter(checkpoints=True).count(), 1)
        self.assertEqual(Post.objects.get(id=self.post.pk).checkpoints, True)
        self.assertEqual(Post.objects.get(id=self.post.pk).checkpoint_set.count(), 1)
        