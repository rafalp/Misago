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
     
    def make_request(self, user=None):
        request = self.factory.get('/customer/details')
        request.session = SessionMock()
        request.user = user
        request.META['HTTP_USER_AGENT'] = 'TestAgent'
        return request
        
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
        request = self.make_request(self.user_alt)
        
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
    
    def test_threads_merge(self):
        """Check if threads are correctly merged"""
        # Create second thread
        self.thread_b = create_thread(self.forum)
        self.post_b = create_post(self.thread_b, self.user)
        
        # Merge threads
        self.thread_b.merge_with(self.thread, 1)
        self.thread_b.delete()
        self.thread.merges += 1
        self.thread.save(force_update=True)
        
        # See if merger was correct
        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(Post.objects.count(), 2)
        last_post = Post.objects.order_by('-id')[:1][0]
        self.assertEqual(last_post.thread_id, self.thread.pk)
        self.assertEqual(last_post.merge, 1)
                
        # Create third thread
        self.thread_c = create_thread(self.forum)
        self.post_c = create_post(self.thread_c, self.user)
              
        # Merge first thread into third one
        self.thread.merge_with(self.thread_c, 1)
        self.thread.delete()

        # See if merger was correct
        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(Post.objects.count(), 3)
        last_post = Post.objects.get(id=last_post.pk)
        self.assertEqual(last_post.thread_id, self.thread_c.pk)
        self.assertEqual(last_post.merge, 2)
        
    def test_threads_move_checkpoints(self):
        """Check if post_move correctly handles checkpoints"""
        # Create thread with two posts
        self.thread_b = create_thread(self.forum)
        self.post_b = create_post(self.thread_b, self.user)
        self.post_c = create_post(self.thread_b, self.user)
        
        # Create an instance of a GET request.
        request = self.make_request(self.user)
        
        # Add checkpoint to post c
        self.post_c.set_checkpoint(request, 'locked')
        self.post_c.save(force_update=True)
        
        # Move post and sync threads
        self.post_c.move_to(self.thread)
        self.post_c.save(force_update=True)
        self.thread.sync()
        self.thread.save(force_update=True)
        self.thread_b.sync()
        self.thread_b.save(force_update=True)
        
        # See threads and post counters
        self.assertEqual(Thread.objects.count(), 2)
        self.assertEqual(Post.objects.count(), 3)
        
        # Refresh post b
        self.post_b = Post.objects.get(id=self.post_b.pk)
        
        # Check if post b has post's c checkpoints
        self.assertEqual(self.post_b.checkpoints, True)
        self.assertEqual(self.post_b.checkpoint_set.count(), 1)
