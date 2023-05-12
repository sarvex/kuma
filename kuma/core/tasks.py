from celery.task import task

from django.db import connection, transaction
from django.contrib.sessions.models import Session
from django.utils import timezone

import constance.config

from .cache import memcache
from .models import IPBan


LOCK_ID = 'clean-sessions-lock'
LOCK_EXPIRE = 60 * 5


def get_expired_sessions(now):
    return (Session.objects.filter(expire_date__lt=now)
                           .order_by('expire_date'))


@task
def clean_sessions():
    """
    Queue deleting expired session items without breaking poor MySQL
    """
    now = timezone.now()
    logger = clean_sessions.get_logger()
    chunk_size = constance.config.SESSION_CLEANUP_CHUNK_SIZE

    if memcache.add(LOCK_ID, now.strftime('%c'), LOCK_EXPIRE):
        total_count = get_expired_sessions(now).count()
        delete_count = 0
        logger.info(
            f'Deleting the {chunk_size} of {total_count} oldest expired sessions'
        )
        try:
            cursor = connection.cursor()
            delete_count = cursor.execute("""
                DELETE
                FROM django_session
                WHERE expire_date < NOW()
                ORDER BY expire_date ASC
                LIMIT %s;
                """, [chunk_size])
            transaction.commit_unless_managed()
        finally:
            logger.info(f'Deleted {delete_count} expired sessions')
            memcache.delete(LOCK_ID)
            expired_sessions = get_expired_sessions(now)
            if expired_sessions.exists():
                clean_sessions.apply_async()
    else:
        logger.error(
            f'The clean_sessions task is already running since {memcache.get(LOCK_ID)}'
        )


@task
def delete_old_ip_bans(days=30):
    IPBan.objects.delete_old(days=days)
