# from requests import Response
import csv

from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files import File
from .ChainData import ChainData


# from .server.application.data_check.main import ChainData


class LastBlock(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        # usernames = [user.username for user in User.objects.all()]
        ch = ChainData(url='https://gnfd-testnet-fullnode-tendermint-us.bnbchain.org/')
        # ch.get_block_num()
        return Response({"current_block": ch.get_block_num()})


class AccountView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        # usernames = [user.username for user in User.objects.all()]
        ch = ChainData(url='https://gnfd-testnet-fullnode-tendermint-us.bnbchain.org/')
        with open('static/data_check/accounts_num.csv', 'r', newline='') as csvfile:

            reader = csv.DictReader((csvfile))
            current =  int(ch.get_accounts_num())
            old = int(next(reader)['account_num'])
            percentage =  (current - old) / old * 100
        # ch.get_accounts_num()
        return Response({"account_num": current, "percent": percentage})


class BandwidthView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        # usernames = [user.username for user in User.objects.all()]
        ch = ChainData(url='https://gnfd-testnet-fullnode-tendermint-us.bnbchain.org/')
        bandwidth = ch.get_bandwidth()
        return Response(bandwidth)


class LatencyView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        # usernames = [user.username for user in User.objects.all()]
        ch = ChainData(url='https://gnfd-testnet-fullnode-tendermint-us.bnbchain.org/')
        latency = ch.get_latency()
        return Response(latency)


class UptimeView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        # usernames = [user.username for user in User.objects.all()]
        ch = ChainData(url='https://gnfd-testnet-fullnode-tendermint-us.bnbchain.org/')

        latency = ch.get_uptime()
        return Response(latency)


class SCView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        # usernames = [user.username for user in User.objects.all()]
        ch = ChainData(url='https://gnfd-testnet-fullnode-tendermint-us.bnbchain.org/')

        latency = ch.get_sc()
        return Response(latency)