def get_model():
    from redditclone.models import MPTTComment
    return MPTTComment

def get_form():
    from redditclone.forms import MPTTCommentForm
    return MPTTCommentForm