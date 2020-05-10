from django.db import models
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):

    ''' newer versions of Django > 1.11 will have an error on this line
        when on not using on_delete parameter inside Foreign_Key '''
    ''' used auth.User as at-least one valid user i.e. user himself will be present as author'''
    author = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)

    title = models.CharField(max_length=200)
    text = models.TextField()
    # dont call timezone.now() function, it should be timezone.now, as we dont have to execute it here
    created_date = models.DateTimeField(default=timezone.now)

    ''' blank=True when we dont want to publish it yet '''
    ''' null=True when we dont have publication date whatsoever, leaving it empty '''
    published_date = models.DateTimeField(blank=True, null=True)

    ''' if publish button will get a hit, then that current time will be saved '''
    def publish(self):
        # we will use timezone.now() as a function as need to execute it here
        self.published_date = timezone.now()
        self.save()

    ''' there will be some list of comments, some will be approved and some may not '''
    ''' here filtering of comments are done on the basis of if they are approved and show them on this website '''
    ''' approved_comment is coming from Comment's class approved_comment field (as Comment is Foreign key to Post) '''
    def approve_comments(self):
        self.comments.filter(approved_comment=True)

    ''' after the post is created where should the post go ? so use get_absolute_url() '''
    ''' post should go to details page with the primary key of the post just created '''
    ''' used pk as we need to go to the specific post for which need to use pk (also used in urls.py '''
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


# all comments associated to the post
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)    # ---> 1111
    author = models.CharField(max_length=200)
    text = models.TextField()
    # dont call timezone.now() function, it should be timezone.now, as we dont have to execute it here
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    ''' Its like publish function '''
    def approve(self):
        self.approved_comment = True
        self.save()

    ''' after the post is created where should the post go ? so use get_absolute_url() '''
    ''' post should go to list-page (no pk as all posts are shown in page having list of posts) '''
    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text


