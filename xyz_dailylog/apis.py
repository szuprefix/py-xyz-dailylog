# -*- coding:utf-8 -*-
from __future__ import division, unicode_literals

from six import text_type
from xyz_restful.mixins import UserApiMixin
from xyz_util.statutils import do_rest_stat_action, using_stats_db
from rest_framework.response import Response

__author__ = 'denishuang'

from . import models, serializers, stats, helper
from rest_framework import viewsets, decorators, status, permissions
from xyz_restful.decorators import register, register_raw


@register()
class DailyLogViewSet(UserApiMixin, viewsets.ModelViewSet):
    queryset = models.DailyLog.objects.all()
    serializer_class = serializers.DailyLogSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'the_date': ['exact', 'gte', 'lte', 'range'],
    }

    @decorators.action(['POST'], detail=False)
    def write(self, request):
        user = request.user
        for k, v in request.data.items():
            log, created = models.DailyLog.objects.get_or_create(user=user, the_date=k)
            log.context.update(v)
            log.save()
        return Response({'detail': 'success'})


@register()
class StatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = using_stats_db(models.Stat.objects.all())
    serializer_class = serializers.StatSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'the_date': ['exact', 'gte', 'lte', 'range'],
        'metics': ['exact'],
        'owner_id': ['exact', 'isnull']
    }

    @decorators.action(['get'], detail=False)
    def stat(self, request):
        return do_rest_stat_action(self, stats.stats_stat)


@register()
class RecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = using_stats_db(models.Record.objects.all())
    serializer_class = serializers.RecordSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'the_date': ['exact', 'gte', 'lte', 'range'],
        'metics': ['exact'],
        'owner_id': ['exact', 'isnull'],
        'owner_type': ['exact', ],
        'user': ['exact', ],
        'user_group': ['exact', ],
        'owner_group': ['exact', ]
    }

    @decorators.action(['get'], detail=False)
    def stat(self, request):
        return do_rest_stat_action(self, stats.stats_record)


@register()
class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = models.Performance.objects.all()
    serializer_class = serializers.PerformanceSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'update_time': ['exact', 'gte', 'lte', 'range'],
        'owner_id': ['exact', 'isnull', 'in'],
        'owner_type': ['exact', ],
        'user': ['exact', ],
        'user_group': ['exact', ],
        'owner_group': ['exact', ]
    }
    search_fields = ['owner_name', 'user_name', 'user_group', 'owner_group']

    @decorators.action(['GET'], detail=False)
    def read(self, request):
        p = helper.get_performance(request.query_params, request.user)
        return Response(serializers.PerformanceSerializer(instance=p).data)

    @decorators.action(['POST'], detail=False)
    def write(self, request):
        p = helper.save_performance(request.data, request.user)
        return Response(serializers.PerformanceSerializer(instance=p).data)


@register_raw(path='dailylog/object')
class ObjectViewSet(viewsets.ViewSet):

    @decorators.action(['get', 'post'], detail=False, permission_classes=[])
    def views(self, request):
        from .stores import ObjectLog
        ol = ObjectLog()
        if request.method == 'POST':
            model = request.data.get('model')
            id = request.data.get('id')
            ol.log(model, id)
            return Response({'detail': 'ok'}, status=status.HTTP_201_CREATED)
        else:
            model = request.query_params.get('model')
            ids = [int(a.strip()) for a in request.query_params.get('ids').split(',') if a.strip()]
            cs = ol.find(model, ids)
            d = dict([(a['_id'], a.get('count', 0)) for a in cs])
            return Response({'detail': d})

    @decorators.action(['post'], detail=False, permission_classes=[])
    def log(self, request):
        from .stores import ObjectLog
        ol = ObjectLog()
        if request.method == 'POST':
            model = request.data.get('model')
            id = request.data.get('id')
            metics = request.data.get('metics')
            ol.log(model, id, metics=metics)
            return Response({'detail': 'ok'}, status=status.HTTP_201_CREATED)

    @decorators.action(['post'], detail=False, permission_classes=[])
    def user(self, request):
        from .stores import ObjectLog
        ol = ObjectLog()
        if request.method == 'POST':
            model = 'auth.user'
            id = request.user.id
            metics = request.data.get('metics')
            delta = request.data.get('delta', 1)
            ol.log(model, id, metics=metics, delta=delta)
            return Response({'detail': 'ok'}, status=status.HTTP_201_CREATED)


@register_raw(path='dailylog/user')
class UserCounterSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @decorators.action(['get', 'post'], detail=False)
    def objects(self, request):
        from .stores import UserLog
        ul = UserLog()
        search = {'id': int(request.user.id)}
        if request.method == 'POST':
            fs = dict([(a, 1) for a in request.data.get('objects')])
            fs['_id'] = 0
            rs = ul.collection.find_one(search, fs)
            return Response({'objects': rs or {}})
        else:
            qs = request.query_params
            ct = qs.get('content_type')
            ids = qs.get('ids').split(',')
            fs = dict([('%s.%s' % (ct, id), 1) for id in ids])
            fs['_id'] = 0
            rs = ul.collection.find_one({'id': int(request.user.id)}, fs)
            return Response({'objects': rs and rs.get(ct) or []})

    @decorators.action(['post'], detail=False)
    def add_to_set(self, request):
        uid = request.user.id
        if not uid:
            return Response({'detail': 0})
        from .stores import UserLog
        ul = UserLog()
        ds = request.data
        r = ul.add_to_set({'id': int(request.user.id)}, ds.get('setvalue'))
        return Response({'detail': r}, status=status.HTTP_201_CREATED)

    @decorators.action(['get', 'post'], detail=False)
    def max(self, request):
        uid = request.user.id
        if not uid:
            return Response({'detail': 0})
        from .stores import UserLog
        ul = UserLog()
        if request.method == 'POST':
            ds = request.data
            metics=ds.get('metics')
            if isinstance(metics, text_type):
                metics = {metics: int(ds.get('value', 1))}
            r = {}
            for k, v in metics.items():
                r[k] = ul.max(request.user.id, metics=k, value=v)
            return Response({'detail': r}, status=status.HTTP_201_CREATED)
        else:
            qs = request.query_params
            mt = qs.get('metics')
            return Response({mt: ul.get(request.user.id, metics=mt)})

    @decorators.action(['get', 'post'], detail=False)
    def set(self, request):
        uid = request.user.id
        if not uid:
            return Response({'detail': 0})
        from .stores import UserLog
        ul = UserLog()
        if request.method == 'POST':
            ds = request.data
            r = ul.set(request.user.id, metics=ds.get('metics'), value=int(ds.get('value', 1)))
            return Response({'detail': r}, status=status.HTTP_201_CREATED)


    @decorators.action(['get', 'post'], detail=False)
    def count(self, request):
        uid = request.user.id
        if not uid:
            return Response({'detail': 0})
        from .stores import UserLog
        ul = UserLog()
        if request.method == 'POST':
            ds = request.data
            r = ul.log(request.user.id, metics=ds.get('metics'), delta=ds.get('delta', 1))
            return Response({'detail': r}, status=status.HTTP_201_CREATED)
        else:
            qs = request.query_params
            mt = qs.get('metics')
            return Response({mt: ul.get(request.user.id, metics=mt)})

    @decorators.action(['post'], detail=False)
    def log(self, request):
        uid = request.user.id
        if not uid:
            return Response({'detail': 0})
        from .stores import UserLog
        st = UserLog()
        if request.method == 'POST':
            ds = request.data
            metics = ds.get('metics')
            delta = ds.get('delta', 1)
            r = st.log(uid, metics=metics, delta=delta)
            from .signals import user_log
            user_log.send_robust(sender=self, user_id=uid, metics=metics, delta=delta)
            return Response({'detail': r}, status=status.HTTP_201_CREATED)

    @decorators.action(['post'], detail=False)
    def daily(self, request):
        uid = request.user.id
        if not uid:
            return Response({'detail': 0})
        from .stores import DailyLog
        st = DailyLog()
        if request.method == 'POST':
            ds = request.data
            metics = ds.get('metics')
            model = ds.get('model')
            delta = ds.get('delta', 1)
            r = st.log(uid, model, metics=metics, delta=delta)
            from .signals import user_log
            user_log.send_robust(sender=self, user_id=uid, model=model, metics=metics, delta=delta)
            return Response({'detail': r}, status=status.HTTP_201_CREATED)
