"""
  Time : 2020-02-23 07:58:30
  Author : Vincent
  FileName: mysql_orm.py
  Software: PyCharm
  Last Modified by: Vincent
  Last Modified time: 2020-02-23 07:58:30
"""
import re
import time
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, Integer, Float, String, Text, ForeignKey, DateTime, TIMESTAMP, UniqueConstraint, Index
from sqlalchemy.sql import func, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()               # 表格对象基类

# logging.basicConfig(filename='sqlalchemy.log',
#                         format="%(asctime)s %(name)s:%(levelname)s:%(module)s:%(funcName)s:"
#                                "%(processName)s:%(process)d:%(message)s")
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)


class Institution(Base):
    """
    机构信息表类
    """
    __tablename__ = 'dyf_off_oper'                # 表名称
    company_num = Column(Integer, primary_key=True, nullable=False, autoincrement=True, comment='机构编号')      # primary_key=True设置主键
    company_name = Column(String(32), comment='机构名称')
    register_time = Column(TIMESTAMP, nullable=True, server_default=func.now(), comment='注册时间')
    status = Column(Integer, server_default=text('0'), comment='0 使用中,1停用')
    company_pass = Column(String(50), comment='密码')
    company_type = Column(Integer, server_default=text('0'), comment='公司类型  0 康美药材编码医院,1 物流公司,2 自身药材编码医院 3其他对接机构')
    storagetype = Column(Integer, server_default=text('10000'), comment='仓库 10000 广州煎煮中心 10001 深圳煎煮中心')
    is_doc_outh = Column(Integer, server_default=text('0'), comment='提供给第三方移动网络平台医生认证 0 不需要，1 需要')
    is_send_msg = Column(Integer, server_default=text('0'), comment='0发短信,1不发短信')
    salesman = Column(String(20), comment='业务员')
    sales_tel = Column(String(20), comment='业务员电话')
    his_abutment = Column(String(20), comment='医院对接人')
    his_abutment_tel = Column(String(20), comment='医院对接人电话')
    his_grade = Column(String(50), comment='医院的分类比如三甲医院、二甲医院、社区医院')
    his_addr = Column(String(255), comment='医院地址')
    business_practice_name = Column(String(1000), comment='营业执照')
    medical_licensing_license_name = Column(String(1000), comment='医疗机构执业许可证')
    distribution_description = Column(String(255), comment='配送时段描述')
    default_consignee = Column(String(255), comment='默认收货人')
    default_tel = Column(String(255), comment='默认收货人电话')
    defalut_addr = Column(String(255), comment='默认收货地址')
    defalut_djdj = Column(Float, server_default=text('2.5'), comment='默认代煎价格')
    isOnline = Column(Integer, server_default=text('0'), comment='对接完成:0是未上线，1是已上线(目前数据不准确,需要实时更新)')
    oper_id = Column(Integer, comment='主要记录修改者id,方便追溯')
    short_name = Column(String(255), comment='简称')
    platform_type = Column(Integer, server_default=text('0'), comment='订单煎煮中心分配规则:0 默认 ,1 按医疗机构 ,2 按地址')


class Order(Base):
    """
    订单表类
    """
    __tablename__ = 'dyf_order'
    order_id = Column(String(36), nullable=False, primary_key=True, comment='订单id')
    create_time = Column(TIMESTAMP(timezone=False), server_default=func.now(), comment='订单创建时间')
    source_id = Column(Integer, nullable=False, comment='订单来源 机构编码')
    order_time = Column(String(25), comment='处方生成时间')
    treat_card = Column(String(50), comment='诊疗卡号')
    reg_num = Column(String(50), nullable=False, comment='挂单号')
    addr_str = Column(String(120), nullable=False, comment='收货地址')
    provinces = Column(String(10), comment='省份')
    city = Column(String(10), comment='城市')
    zone = Column(String(10), comment='区')
    consignee = Column(String(20), nullable=False, comment='收货人')
    con_tel = Column(String(50), nullable=False, comment='收货人电话')
    send_goods_time = Column(String(25), comment='送货时间')
    storagetype = Column(Integer, comment='仓库')
    is_hos_addr = Column(Integer, nullable=False, comment='是否送医院 0 未知, 1 送医院,2 送病人家里')
    updata_time = Column(TIMESTAMP(timezone=False), nullable=False, comment='数据更新时间')


class Prescription(Base):
    """
    处方表类
    """
    __tablename__ = 'dyf_prescriptions'
    prescri_id = Column(String(36), nullable=False, primary_key=True, comment='处方ID')
    order_id = Column(String(36), nullable=False, comment='订单id')
    user_name = Column(String(20), nullable=False, comment='患者姓名')
    age = Column(Integer, nullable=False, comment='患者年龄')
    gender = Column(Integer, nullable=False, comment='患者性别 0 女，1 男，2 未知(病人没有登记性别的情况下)')
    tel = Column(String(50), nullable=False, comment='患者电话')
    is_pregnant = Column(Integer, comment='是否为孕妇 0 非孕妇，1 孕妇, 2 未知')
    is_hos = Column(Integer, nullable=False, comment='处方来源类型 0 默认,1门诊,2住院,3 其他')
    is_suffering = Column(Integer, nullable=False, comment='是否煎煮 取值范围：0 否，1 是')
    amount = Column(Integer, nullable=False, comment='数量')
    suffering_num = Column(Integer, nullable=False, comment='煎煮剂数')
    ji_fried = Column(Integer, nullable=False, comment='几煎')
    prescri_type = Column(Integer, comment='处方类型 0:中药，1:西药，2:膏方，3:丸剂，5:散剂，7:免煎颗粒')
    is_within = Column(Integer, nullable=False, comment='服用方式 0 内服，1 外用')
    other_pres_num = Column(String(50), nullable=False, comment='医院处方号')
    special_instru = Column(String(100), comment='处方特殊说明 诊断信息')
    bed_num = Column(String(50), comment='床位号')
    hos_depart = Column(String(50), comment='医院科室')
    hospital_num = Column(String(50), comment='住院号')
    disease_code = Column(String(50), comment='病区号')
    doctor = Column(String(50), nullable=False, comment='医生姓名')
    paste_desc_file = Column(String(100), comment='膏方描述')
    prescript_remark = Column(String(120), comment='处方备注')
    per_pack_num = Column(Integer, comment='每剂几包')
    per_pack_dose = Column(Integer, comment='每包多少ml')
    medication_methods = Column(String(50), comment='用药方法')
    medication_instruction = Column(String(50), comment='用药指导')
    create_time = Column(TIMESTAMP(timezone=False), server_default=func.now(), comment='处方创建时间')
    updata_time = Column(TIMESTAMP(timezone=False), nullable=False, comment='数据更新时间')


class PresDetails(Base):
    """
    处方明细(药材)表类
    """
    __tablename__ = 'dyf_prescriptions_details'
    prescription_details_id = Column(String(36), primary_key=True, nullable=False, comment='处方详情ID')
    prescri_id = Column(String(36), nullable=False, comment='处方ID')
    medicines = Column(String(100), nullable=False,comment='药品名')
    goods_num = Column(String(100), comment='药材编号')
    dose = Column(String(10), server_default='0.00', comment='剂量')
    unit = Column(String(50), nullable=False, comment='单位')
    m_usage = Column(String(100), comment='药品特殊煎法')
    status = Column(Integer, server_default='0', comment='状态')
    type = Column(Integer, server_default='0', comment='药材类型：0 中药，1西药')
    goods_norms = Column(String(100), comment='药品规格')
    goods_orgin = Column(String(100), comment='药品产地')
    remark = Column(String(100), comment='备注')
    dose_that = Column(String(100), comment='药品注意事项说明')
    company_num = Column(String(50), comment='机构编号')
    unit_price = Column(Float, server_default='0.00', comment='医院药品销售单价')
    MedPerDos = Column(String(20), comment='用量(剂量)eg:2片/次(每次两片)')
    MedPerDay = Column(String(20), comment='执行频率(频次)（eg:一日3次）')
    create_time = Column(TIMESTAMP(timezone=False), server_default=func.now(), comment='创建时间')
    updata_time = Column(TIMESTAMP(timezone=False), nullable=False, comment='数据更新时间')


class Address(Base):
    """
    地址 custom_addr 表类
    """
    __tablename__ = 'dyf_custom_addr'
    addr_id = Column(Integer, nullable=False, primary_key=True, comment='地址id')
    username = Column(String(30), nullable=False, comment='患者姓名')
    treat_card = Column(String(50), nullable=False, comment='诊疗卡号')
    pres_num = Column(String(50), nullable=False, comment='医院处方号')
    consignee = Column(String(30), nullable=False, comment='收货人')
    con_tel = Column(String(50), nullable=False, comment='收货人电话')
    provinces = Column(String(10), nullable=False, comment='省份')
    city = Column(String(10), nullable=False, comment='城市')
    zone = Column(String(10), nullable=False, comment='区县')
    addr_detail = Column(String(50), nullable=False, comment='详细地址')
    fee = Column(Float, nullable=False, comment='物流费用')


def get_session():
    """
    初始化数据库连接,返回 engine 和 session
    :return: (engine,session)
    engine = create_engine('dialect+driver://username:password@host:port/database')
        [dialect -- 数据库类型, driver -- 数据库驱动选择, username -- 数据库用户名,
        password -- 用户密码, host 服务器地址, port 端口, database 数据库]
    """
    engine = create_engine(
        # "mysql+pymysql://root:KM*021191@localhost:3306/zhyf?charset=utf8",
        "mysql+mysqlconnector://root:KM*021191@localhost:3306/zhyf?charset=utf8",
        max_overflow=0,         # 超过连接池大小外最多创建的连接
        pool_size=5,            # 连接池大小
        pool_timeout=30,        # 池中没有线程最多等待的时间，否则报错
        pool_recycle=3600       # 多久之后对线程池中的线程进行一次连接的回收（重置）
        )

    DBSession = sessionmaker(bind=engine)  # 创建会话的类
    session = DBSession()
    return engine, session


def init_db(en):
    """
    根据类创建数据库表
    :return:
    """
    Base.metadata.create_all(en)


def drop_db(en):
    """
    根据类 删除数据库表
    :return:
    """
    Base.metadata.drop_all(en)  # 这行代码很关键哦！！ 读取继承了Base类的所有表在数据库中进行删除表


def saveAccountInfo_to_db(dict_data):
    '''
    保存账号信息
    :param dict_data:
    :return:
    '''


def makeorder_to_db(dict_data):
    '''
    保存订单
    :param dict_data: 接收到的订单字典数据
    :return: 数据是否写入成功
    '''
    order_session = get_session()[1]
    order_all_list = order_session.query(Order).all()
    logging.info(order_all_list)
    logging.info("订单表 dyf_order 中原记录条数:%s" % len(order_all_list))
    order_id = 'KM' + time.strftime('%y%m%d', time.localtime()) + format(len(order_all_list) + 1, '0>5')
    logging.info('生成订单号:%s' % order_id)
    prescri_all_list = order_session.query(Prescription).filter(Prescription.order_id == order_id).all()
    if len(prescri_all_list) == 0:
        order_information = Order(order_id=order_id, source_id=dict_data['company_num'],
                                  order_time=dict_data['order_time'], treat_card=dict_data.get('treat_card', None),
                                  reg_num=dict_data['reg_num'], addr_str=dict_data['addr_str'],
                                  provinces=dict_data['addr_str'].split(',')[0],
                                  city=dict_data['addr_str'].split(',')[1],
                                  zone=dict_data['addr_str'].split(',')[2],
                                  consignee=dict_data['consignee'], con_tel=dict_data['con_tel'],
                                  send_goods_time=dict_data.get('send_goods_time', ''), storagetype=10000,
                                  is_hos_addr=dict_data.get('is_hos_addr', 0))
        prescri_information = Prescription(prescri_id=order_id+'-1', order_id=order_id,
                                           user_name=dict_data['user_name'],
                                           age=dict_data['age'], gender=dict_data['gender'], tel=dict_data['tel'],
                                           is_pregnant=dict_data.get('is_pregnant', 2),
                                           is_hos=dict_data.get('is_hos', 0),
                                           is_suffering=dict_data['is_suffering'], amount=dict_data['amount'],
                                           suffering_num=dict_data['suffering_num'],
                                           ji_fried=dict_data.get('ji_fried', 1),
                                           prescri_type=dict_data['prescri_type'], is_within=dict_data['is_within'],
                                           other_pres_num=dict_data['other_pres_num'],
                                           special_instru=dict_data['special_instru'],
                                           bed_num=dict_data.get('bed_num', None),
                                           hos_depart=dict_data.get('hos_depart', None),
                                           hospital_num=dict_data.get('hospital_num', None),
                                           disease_code=dict_data.get('disease_code', None), doctor=dict_data['doctor'],
                                           paste_desc_file=dict_data.get('paste_desc_file', None),
                                           prescript_remark=dict_data.get('prescript_remark', None),
                                           per_pack_num=dict_data['per_pack_num'],
                                           per_pack_dose=dict_data.get('per_pack_dose', 200),
                                           medication_methods=dict_data['medication_methods'],
                                           medication_instruction=dict_data['medication_instruction'])
        pres_detail_information_list = []
        medicine_count = len(dict_data['medicines'])
        for num in range(medicine_count):
            pres_detail_information = PresDetails(prescription_details_id=order_id+'-1-'+str(num+1),
                                                  prescri_id=order_id+'-1', medicines=dict_data['medicines'][num],
                                                  goods_num=dict_data['goods_num'][num], dose=dict_data['dose'][num],
                                                  unit=dict_data['unit'][num], m_usage=dict_data['m_usage'][num],
                                                  goods_norms=dict_data.get('goods_norms', [None]*medicine_count)[num],
                                                  goods_orgin=dict_data.get('goods_orgin', [None]*medicine_count)[num],
                                                  remark=dict_data.get('remark', [None]*medicine_count)[num],
                                                  dose_that=dict_data.get('dose_that', [None]*medicine_count)[num],
                                                  company_num=dict_data['company_num'],
                                                  unit_price=dict_data['unit_price'][num],
                                                  MedPerDos=dict_data.get('MedPerDos', [None]*medicine_count)[num],
                                                  MedPerDay=dict_data.get('MedPerDay', [None]*medicine_count)[num])
            pres_detail_information_list.append(pres_detail_information)
        logging.info("开始连接数据库提交数据")
        order_session.add(order_information)
        order_session.add(prescri_information)
        logging.info('prescri_details:%s' % pres_detail_information_list)
        order_session.add_all(pres_detail_information_list)
        try:
            order_session.commit()         # 尝试提交数据库事务
            logging.info('数据库数据提交成功')
            # return {"code": 200, "status": True, "message": "写入数据库成功"}
            return {'resultCode': 0, 'description': '成功', 'state': 'success', 'reg_num': order_information.reg_num,
                    'IsSuccess': 'true', 'message': '成功', 'orderid': order_information.order_id,
                    'prescriptionIds': prescri_information.prescri_id
                    }
        except SQLAlchemyError as e:
            order_session.rollback()
            logging.info(e)
            return {'resultCode': 500, 'description': '失败', 'state': 'fail', 'reg_num': order_information.reg_num,
                    'IsSuccess': 'false', 'message': str(e)}


def saveaddr_to_db(dict_data):
    '''
    保存地址信息
    :param dict_data: 接收到的字典数据
    :return:
    '''
    addr_session = get_session()[1]
    addr_information = Address(username=dict_data['username'], treat_card=dict_data['treat_card'],
                               pres_num=dict_data['pres_num'], consignee=dict_data['consignee'],
                               con_tel=dict_data['con_tel'], provinces=dict_data['provinces'], city=dict_data['city'],
                               zone=dict_data['zone'], addr_detail=dict_data['addr_detail'],
                               fee=dict_data.get('fee', 0.00))
    logging.info("开始连接数据库保存地址信息")
    addr_session.add(addr_information)
    try:
        addr_session.commit()  # 尝试提交数据库事务
        logging.info('地址信息保存成功')
        return {'resultCode': 0, 'description': '成功', 'status': 'success', 'message': '地址保存成功！'}
    except SQLAlchemyError as e:
        addr_session.rollback()
        logging.info(e)
        return {'resultCode': 500, 'description': '失败', 'status': 'fail', 'message': str(e)}


if __name__ == '__main__':
    es = get_session()
    # init_db(es[0])                    # 执行创建
    drop_db(es[0])
    # makeorder_to_db()
