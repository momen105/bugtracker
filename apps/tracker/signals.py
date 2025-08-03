from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BugModel, CommentModel
from .utils import *
from .serializers import *

@receiver(post_save, sender=BugModel)
def bug_created_or_updated(sender, instance, created, **kwargs):
    bug_ser = BugSerializer(instance)
    action = str("created" if created else "updated")
   
    notify_project(instance.project.id, bug_ser.data,"bug",action)


# Show data from the serializer directly.
# But,i want to display it in another format or customized way.
@receiver(post_save, sender=CommentModel)
def comment_created(sender, instance, created, **kwargs):
    if created:
        bug = instance.bug
        data = {
            "type": "comment_added",
            "comment_id": instance.id,
            "message": instance.message,
            "commenter": instance.commenter.name,
            "bug_id": bug.id,
            "bug_title": bug.title,
        }

        # Notify bug creator and assigned_to users
        users_to_notify = set()
        if bug.created_by:
            users_to_notify.add(bug.created_by.id)
        if bug.assigned_to:
            users_to_notify.add(bug.assigned_to.id)

        for user_id in users_to_notify:
            notify_users(user_id, data)