from django.db import models
from django_comments.models import Comment
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User

# Create your models here.

class Tread(models.Model):

    title = models.CharField(max_length=100)
    comment = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class MPTTComment(MPTTModel, Comment):
    """ Threaded comments - Add support for the parent comment store and MPTT traversal"""

    # a link to comment that is being replied, if one exists
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)

    class MPTTMeta:
        # comments on one level will be ordered by date of creation
        order_insertion_by=['submit_date']

    class Meta:
        ordering=['tree_id','lft']