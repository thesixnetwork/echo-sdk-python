#  from pyeos_client.EOSChainApi import ChainAPI
#  from pyeos_client.EOSWalletApi import WalletAPI
#  from pyeos_client.NodeosConnect import RequestHandlerAPI
import datetime as dt
import json
import os
import uuid
from datetime import datetime, timezone

import eospy.cleos
import pytz


class Chain(object):
    """
    Chain class
    """
    def __init__(self, private_key=None, host_url=None):
        """
        host_url require  host url of sixchain
        private_key require wallet
        """
        self.private_key = private_key
        self.host_url = host_url
        self.ce = eospy.cleos.Cleos(url=self.host_url)

    def get_id(self, authorization, owner):
        """
        owner - Required : string : name of wallet
        authorization - Required : Array(dict)
            - ex: [{"actor": "bob1","permission": "active"}]
        """
        ce = self.ce
        payload = {
            "account": "assets",
            "name": "newasset",
            "authorization": authorization,
        }

        arguments = {
            "creator": owner,
        }
        data = ce.abi_json_to_bin(payload["account"], payload["name"],
                                  arguments)
        payload['data'] = data['binargs']
        trx = {"actions": [payload]}
        trx['expiration'] = str(
            (dt.datetime.utcnow() +
             dt.timedelta(seconds=60)).replace(tzinfo=pytz.UTC))
        key = eospy.keys.EOSKey(self.private_key)
        resp = ce.push_transaction(trx, key, broadcast=True)
        assetid = resp["processed"]["action_traces"][0]["inline_traces"][1][
            "act"]["data"]["assetid"]
        #  newid = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
        return assetid

    def push_transaction(self, owner, authorization, digital_content):
        """
        upload digital content to server
        owner - Required : string : name of wallet
        authorization - Required : Array(dict)
            - ex: [{"actor": "bob1","permission": "active"}]
        digital_content - Required : Object of Asset Type
          mdata :
           - echo_title  require title show sixecho work
           - echo_image_url option image show sixecho work
           - echo_tags  options  tag show sixecho work
           - echo_parent_id option tag show sixecho work
           - echo_owner option current owner
           - echo_ref_owner option current owner id
           - echo_creator require who is creator asset
           - echo_ref_creator option  who is creator asset id
        """
        ce = self.ce
        payload = {
            "account": "assets",
            "name": "create",
            "authorization": authorization,
        }
        idata = json.dumps({
            "digest": digital_content.digest,
            "sha256": digital_content.sha256,
            "size_file": digital_content.file_size,
            "type": digital_content.type
        })
        mdata = json.dumps(digital_content.meta_media)
        if digital_content.meta_media.get("echo_title") is None:
            raise Exception("Mata must have title")
        arguments = {
            "assetid": self.get_id(authorization, owner),
            "creator": owner,
            "owner": owner,
            "idata": idata,
            "mdata": mdata,
            "requireclaim": 0
        }
        resp = self.__push__(payload, arguments)
        #  data = ce.abi_json_to_bin(payload["account"], payload["name"],
        #  arguments)
        #  payload['data'] = data['binargs']
        #  trx = {"actions": [payload]}
        #  trx['expiration'] = str(
        #  (dt.datetime.utcnow() +
        #  dt.timedelta(seconds=60)).replace(tzinfo=pytz.UTC))
        #  key = eospy.keys.EOSKey(self.private_key)
        #  resp = ce.push_transaction(trx, key, broadcast=True)
        return resp

    def get_transaction(self):
        """
        """
        print("coming soon")

    def transfer(self, authorization, platform, user, asset_id, memo):
        """
          authorization - Required : Array(dict)
              - ex: [{"actor": "bob1","permission": "active"}]
          platform - Required : dict
            from_platform - Required : string
            to_platform - Required : string
          user - Required : dict
            from_user - Required : dict
                echo_owner - Required : string
                echo_ref_owner - Required : string
            to_user - Required : dict
                echo_owner - Required : string
                echo_ref_owner - Required : string
          asset_id - Required : string
          memo - Option - string
        """
        payload = {
            "account": "assets",
            "name": "transfer",
            "authorization": authorization,
        }
        from_user = json.dumps(user["from_user"])
        to_user = json.dumps(user["to_user"])
        arguments = {
            "from": platform["from_platform"],
            "to": platform["to_platform"],
            "fromjsonstr": from_user,
            "tojsonstr": to_user,
            "assetid": asset_id,
            "memo": memo
        }
        resp = self.__push__(payload, arguments)
        return resp

    def trade(self, authorization, platform, user, asset_id, price, memo):
        """
          authorization - Required : Array(dict)
              - ex: [{"actor": "bob1","permission": "active"}]
          platform - Required : dict
            from_platform - Required : string
            to_platform - Required : string
          user - Required : dict
            from_user - Required : dict
                echo_owner - Required : string
                echo_ref_owner - Required : string
            to_user - Required : dict
                echo_owner - Required : string
                echo_ref_owner - Required : string
          asset_id - Required : string
          price - Required : float
          memo - Option - string
        """
        payload = {
            "account": "assets",
            "name": "trade",
            "authorization": authorization,
        }
        from_user = json.dumps(user["from_user"])
        to_user = json.dumps(user["to_user"])
        arguments = {
            "from": platform["from_platform"],
            "to": platform["to_platform"],
            "fromjsonstr": from_user,
            "tojsonstr": to_user,
            "assetids": [asset_id],
            "price": price,
            "memo": memo
        }
        resp = self.__push__(payload, arguments)
        return resp

    def update(self, authorization, owner, asset_id, mdata):
        """
        Update Mdata in asset
          authorization - Required : Array(dict)
              - ex: [{"actor": "bob1","permission": "active"}]
          owner - Required : string
          asset_id - Required : string
          mdata - Required : dict
        """
        mdata = json.dumps(mdata)
        payload = {
            "account": "assets",
            "name": "update",
            "authorization": authorization,
        }
        arguments = {
            "owner": owner,
            "asset_id": asset_id,
            "mdata": mdata,
        }
        resp = self.__push__(payload, arguments)
        return resp

    def revoke(self, authorization, owner, asset_id, memo):
        """
         Delete asset
            authorization - Required : Array(dict)
                - ex: [{"actor": "bob1","permission": "active"}]
            owner - Required : string
            asset_id - Required : string
        """
        payload = {
            "account": "assets",
            "name": "revoke",
            "authorization": authorization,
        }
        arguments = {
            "owner": owner,
            "asset_id": asset_id,
            "memo": memo,
        }
        resp = self.__push__(payload, arguments)
        return resp

    def __push__(self, payload, arguments):
        data = self.ce.abi_json_to_bin(payload["account"], payload["name"],
                                       arguments)
        payload['data'] = data['binargs']
        trx = {"actions": [payload]}
        trx['expiration'] = str(
            (dt.datetime.utcnow() +
             dt.timedelta(seconds=60)).replace(tzinfo=pytz.UTC))
        key = eospy.keys.EOSKey(self.private_key)
        resp = self.ce.push_transaction(trx, key, broadcast=True)
        return resp
