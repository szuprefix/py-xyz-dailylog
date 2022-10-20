# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from six import text_type

from . import models
from logging import getLogger

log = getLogger('django')


def do_daily_stat(the_date):
    d = {}
    for l in models.DailyLog.objects.filter(the_date=the_date):
        for k, v in l.context.items():
            ps = k.split('.')
            app, model, mid, category, metric = ps
            am = (app, model)
            mt = "%s.%s" % (category, metric)
            r = d.setdefault(am, {}).setdefault(mid, {}).setdefault(mt, {'v': 0, 'u': 0})
            r['u'] += 1
            r['v'] += v
            r2 = d.setdefault(am, {}).setdefault(None, {}).setdefault(mt, {'v': 0, 'u': 0, 'us': set()})
            r2['us'].add(l.user.id)
            r2['u'] = len(r2['us'])
            r2['v'] += v
    for am, dam in d.items():
        ct = ContentType.objects.get_by_natural_key(am[0], am[1])
        for oid, doid in dam.items():
            for mt, dmt in doid.items():
                models.Stat.objects.update_or_create(
                    the_date=the_date,
                    owner_type=ct,
                    owner_id=oid,
                    metics=mt,
                    defaults=dict(
                        value=dmt['v'],
                        user_count=dmt['u']
                    )
                )
    return d


def gen_dailylog_records(the_date):
    ocache = {}
    for l in models.DailyLog.objects.filter(the_date=the_date):
        user = l.user
        user_name = user.get_full_name()
        user_group = ''
        if hasattr(user, 'as_school_student'):
            user_group = text_type(user.as_school_student.classes.first())
        for k, v in l.context.items():
            ps = k.split('.')
            if len(ps) != 5:
                continue
            app, model, mid, category, metric = ps
            mt = "%s.%s" % (category, metric)
            odata = ocache.setdefault((mt, mid), {})
            if not odata:
                ct = odata['owner_type'] = ContentType.objects.get_by_natural_key(app, model)
                owner = ct.get_object_for_this_type(pk=mid)
                odata['owner_name'] = text_type(owner)
                odata['owner_group'] = ''
                if hasattr(owner, 'owner'):
                    odata['owner_group'] = text_type(owner.owner)
            # else:
            #     print('cached', len(odata))
            try:
                models.Record.objects.update_or_create(
                    the_date=the_date,
                    owner_type=odata['owner_type'],
                    owner_id=mid,
                    metics=mt,
                    user=l.user,
                    defaults=dict(
                        value=v,
                        user_group=user_group,
                        user_name=user_name,
                        **odata
                    )
                )
            except Exception as e:
                import traceback
                log.error('gen_dailylog_records(%s) error: %s', the_date, traceback.format_exc())


def gen_dailylog_records_to_store(the_date):
    from .stores import Record
    rst = Record()
    for l in models.DailyLog.objects.filter(the_date=the_date):
        user = l.user
        user_name = user.get_full_name()
        user_group = ''
        if hasattr(user, 'as_school_student'):
            user_group = text_type(user.as_school_student.classes.first())
        for k, v in l.context.items():
            ps = k.split('.')
            if len(ps) != 5:
                continue
            app, model, mid, category, metric = ps
            mt = "%s.%s" % (category, metric)
            ct = ContentType.objects.get_by_natural_key(app, model)
            owner = ct.get_object_for_this_type(pk=mid)
            owner_name = text_type(owner)
            owner_group = ''
            if hasattr(owner, 'owner'):
                owner_group = text_type(owner.owner)
            try:
                from .stores import UserLog
                rst.upsert(
                    dict(
                        the_date=the_date,
                        owner_type=ct.id,
                        owner_id=mid,
                        metics=mt,
                        user=user.id,
                    ),
                    dict(
                        value=v,
                        owner_name=owner_name,
                        owner_group=owner_group,
                        user_group=user_group,
                        user_name=user_name
                    )
                )
            except Exception as e:
                import traceback
                log.error('gen_dailylog_records_to_store(%s) error: %s', the_date, traceback.format_exc())


def save_performance(d, user):
    ct = ContentType.objects.get(app_label=d['app'], model=d['model'])
    p, created = models.Performance.objects.update_or_create(
        user=user,
        owner_type=ct,
        owner_id=d['owner_id'],
        defaults=dict(
            detail=d['detail']
        ))
    return p


def get_performance(d, user):
    ct = ContentType.objects.get(app_label=d['app'], model=d['model'])
    p, created = models.Performance.objects.get_or_create(user=user, owner_type=ct, owner_id=d['owner_id'], defaults={})
    return p


def log_views(model, id):
    try:
        from .stores import ObjectLog
        ol = ObjectLog()
        ol.log(model, id)
    except:
        import traceback
        log.error('dailylog log_views error: %s', traceback.format_exc())
