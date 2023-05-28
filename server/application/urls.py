from django.urls import path

from .serializers import LastBlock, AccountView, BandwidthView, LatencyView, UptimeView, SCView

urlpatterns = [
    # path('', include(router.urls)),
    path('/current_block', LastBlock.as_view()),
    path('/account_num', AccountView.as_view()),
    path('/bandwidth', BandwidthView.as_view()),
    path('/latency', LatencyView.as_view()),
    path('/uptime', UptimeView.as_view()),
    path('/sc', SCView.as_view())
]