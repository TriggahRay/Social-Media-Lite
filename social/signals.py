# social/signals.py
# Django signals allow certain senders to notify a set of receivers
# when certain actions occur — without the two being directly coupled.
#
# We use signals to automatically create Notification records
# whenever a like, comment, or follow happens — without having
# to manually call Notification.objects.create() in every single view.
#
# Think of signals like event listeners in JavaScript:
# "When X happens, automatically run Y."

from django.db.models.signals import post_save  # Fires AFTER a model record is saved
from django.dispatch import receiver             # Decorator that connects a function to a signal
from .models import Like, Comment, Follow, Notification


@receiver(post_save, sender=Like)
def notify_on_like(sender, instance, created, **kwargs):
    """
    Automatically creates a Notification when a new Like is saved.

    sender   = the model class that triggered the signal (Like)
    instance = the specific Like object that was just saved
    created  = True if this is a new record, False if it was updated

    We only create a notification when created=True because
    likes are either created or deleted — never updated.
    We also skip notification if the user liked their own post.
    """
    if created:
        # Only notify if someone ELSE liked the post.
        # No point notifying yourself that you liked your own post.
        if instance.user != instance.post.user:
            Notification.objects.create(
                user=instance.post.user,        # Post owner receives the notification
                sender=instance.user,           # Person who liked the post
                notification_type='like',
                message=f'{instance.user.username} liked your post.',
                post=instance.post              # Link to the liked post
            )


@receiver(post_save, sender=Comment)
def notify_on_comment(sender, instance, created, **kwargs):
    """
    Automatically creates a Notification when a new Comment is saved.
    Only fires on creation — not when a comment is edited.
    Skips self-comments (commenting on your own post).
    """
    if created:
        if instance.user != instance.post.user:
            Notification.objects.create(
                user=instance.post.user,
                sender=instance.user,
                notification_type='comment',
                message=f'{instance.user.username} commented on your post.',
                post=instance.post
            )


@receiver(post_save, sender=Follow)
def notify_on_follow(sender, instance, created, **kwargs):
    """
    Automatically creates a Notification when a new Follow is saved.
    Only fires when a new follow is created — not on any updates.
    No post field needed since a follow is not tied to a specific post.
    """
    if created:
        Notification.objects.create(
            user=instance.following,            # Person being followed receives notification
            sender=instance.follower,           # Person who followed them
            notification_type='follow',
            message=f'{instance.follower.username} started following you.'
            # No post= here — follow notifications are not linked to a post
        )