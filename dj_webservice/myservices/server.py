#coding:utf-8
"""
  Time : 2020-02-23 07:32:54
  Author : Vincent
  FileName: server.py
  Software: PyCharm
  Last Modified by: Vincent
  Last Modified time: 2020-02-23 07:32:54
"""
import json
import logging
import base64
from spyne import Application, rpc, ServiceBase
from spyne import String, Integer
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from django.views.decorators.csrf import csrf_exempt
from .xml_envelope import XmlEnvelopeTree
from .handle import request_base64_decode
from .map.mysql_orm import init_db, get_session, makeorder_to_db, saveaddr_to_db


# Create your views here.
logging.basicConfig(level=logging.DEBUG, filename='my_server.log',
                        format="%(asctime)s %(name)s:%(levelname)s:%(module)s:%(funcName)s:"
                               "%(processName)s:%(process)d:%(message)s")
logging.getLogger(__name__).setLevel(logging.DEBUG)


class OrderServices(ServiceBase):
    """声明服务的类，类的方法，就是客户端访问的服务，业务逻辑，操作都在这里面"""

    @rpc(String, _returns=String)
    def saveOrderInfo(self, request):
        '''
        保存订单接口
        :param request: 接收的请求
        :return: 订单保存结果
        '''
        logging.info('接收到请求:%s' % request)
        rq_decode = request_base64_decode(request)
        logging.info('请求参数:%s' % rq_decode)
        env_tree = XmlEnvelopeTree(rq_decode)
        dict_data = env_tree.xml_to_dict()
        logging.info('请求体字典数据:%s' % dict_data)
        result = makeorder_to_db(dict_data)
        xml_tree = XmlEnvelopeTree(result)
        logging.info('响应数据：%s' % xml_tree.envelope_encode())
        return base64.b64encode(xml_tree.envelope_encode().encode('utf-8')).decode()

    @rpc(String, _returns=String)
    def acceptUserAddrInfo(self, request):
        '''
        保存推送过来的地址信息接口
        :param request: 接收的请求
        :return: 地址保存结果
        '''
        logging.info('接收到请求:%s' % request)
        rq_decode = request_base64_decode(request)
        logging.info('请求参数:%s' % rq_decode)
        env_tree = XmlEnvelopeTree(rq_decode)
        dict_data = env_tree.xml_to_dict()
        logging.info('请求体字典数据:%s' % dict_data)
        result = saveaddr_to_db(dict_data)
        xml_tree = XmlEnvelopeTree(result)
        logging.info('响应数据：%s' % xml_tree.envelope_encode())
        return base64.b64encode(xml_tree.envelope_encode().encode('utf-8')).decode()


soap_app = Application([OrderServices],
                       tns='webservice_test.myservice.views',
                       # in_protocol=HttpRpc(validator='soft'),
                       # 'SampleServices',
                       in_protocol=Soap11(validator="lxml"),
                       out_protocol=Soap11())
django_app = DjangoApplication(soap_app)
sum_app = csrf_exempt(django_app)
es = get_session()
init_db(es[0])
logging.info("listening to http://127.0.0.1:8000")
logging.info("wsdl is at: http://localhost:8000/OrderServices?wsdl")