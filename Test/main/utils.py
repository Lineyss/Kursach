from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
import logging

class DatabaseHandler(logging.Handler):
    def emit(self, record):
        try:
            level = record.levelname
            message = record.getMessage()
            user = None
            obj = None
            action_flag = None
            
            if hasattr(record, 'request'):
                user = record.request.user if record.request.user.is_authenticated else None
                if hasattr(record, 'object'):
                    obj = record.object

                if level == 'DEBUG':
                    action_flag = ADDITION
                elif level == 'INFO':
                    action_flag = CHANGE
                elif level == 'WARNING':
                    action_flag = CHANGE
                elif level == 'ERROR':
                    action_flag = CHANGE
                elif level == 'CRITICAL':
                    action_flag = DELETION

            if user and obj and action_flag:
                content_type = ContentType.objects.get_for_model(obj)
                log_entry = LogEntry.objects.create(
                    user=user,
                    content_type=content_type,
                    object_id=obj.pk,
                    object_repr=str(obj),
                    action_flag=action_flag,
                    change_message=message,
                )
        except Exception as e:
            print(f"Error saving log: {e}")

logger = logging.getLogger(__name__)

database_handler = DatabaseHandler()
logger.addHandler(database_handler)
