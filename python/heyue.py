#!/usr/bin/python
# coding=UTF-8
import sys
import random
import math
import time
import os
import requests
import configparser
import subprocess
import MySQLdb
import json
import _thread
import uuid
import urllib.request
from urllib.parse import urlencode
import ccxt
from pprint import pprint

thread_alive = {}
pending_order = {}
all_ticker = {}
platform_ticker_time = {}
platform_order_time = {}


def get_conf(name):
    cp = configparser.ConfigParser()
    the_dir = sys.path[0]
    # print(the_dir)
    cp.read(the_dir + '/db.conf')
    return cp.get('db', name)


# 连接数据库
def Conn():
    cp = configparser.ConfigParser()
    the_dir = sys.path[0]
    # print(the_dir)
    cp.read(the_dir + '/db.conf')
    return MySQLdb.connect(host=cp.get('db', 'host'), user=cp.get('db', 'user'), passwd=cp.get('db', 'pass'),
                           db=cp.get('db', 'name'), port=int(cp.get('db', 'port')), charset=cp.get('db', 'charset'))


# 更新显示信息
def updateMsg(robot_id, show_msg):
    conn = Conn()
    cur = conn.cursor()
    update_sql = "update jl_quant_robot set show_msg = '%s' where id = %d" % (
        show_msg, robot_id)
    # print(update_sql)
    cur.execute(update_sql)
    conn.commit()
    cur.close()
    conn.close()


# 更新机器人当前状态

def updateStatus(robot_id, order_status):
    conn = Conn()
    cur = conn.cursor()
    update_sql = "update jl_quant_robot set order_status = %d where id = %d" % (
        order_status, robot_id)
    cur.execute(update_sql)
    conn.commit()
    cur.close()
    conn.close()


# 更新机器人运行参数 张数 是否成交 价格等
def updateValues(robot_id, values_str):
    conn = Conn()
    cur = conn.cursor()
    update_sql = "update jl_quant_robot set values_str = '%s' where id = %d" % (
        values_str, robot_id)
    # print(update_sql)
    cur.execute(update_sql)
    conn.commit()
    cur.close()
    conn.close()


# 更新机器人订单号
def updateOrder(robot_id, order_id):
    conn = Conn()
    cur = conn.cursor()
    update_sql = "update jl_quant_robot set order_id = '%s' where id = %d" % (
        order_id, robot_id)
    cur.execute(update_sql)
    conn.commit()
    cur.close()
    conn.close()


# 更新机器人收益
def updateRevenue(robot_id, revenue):
    conn = Conn()
    cur = conn.cursor()
    update_sql = "update jl_quant_robot set revenue = '%s' where id = %d" % (
        revenue, robot_id)
    # print(update_sql)
    cur.execute(update_sql)
    conn.commit()
    cur.close()
    conn.close()


# 关闭机器人
def disableRobot(robot_id):
    conn = Conn()
    cur = conn.cursor()
    update_sql = "update jl_quant_robot set status = 0 where id = %d" % robot_id
    # print(update_sql)
    cur.execute(update_sql)
    conn.commit()
    cur.close()
    conn.close()


# 平仓
def cleanFinish(robot_id):
    conn = Conn()
    cur = conn.cursor()
    update_sql = "update jl_quant_robot set is_clean = 0 where id = %d" % robot_id
    # print(update_sql)
    cur.execute(update_sql)
    conn.commit()
    cur.close()
    conn.close()


# 插入运行日志
def insertLog(platform, robot_id, uid, log):
    conn = Conn()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(
        "select id,content from jl_quant_robot_log where qrobot_id = %d order by id desc limit 0,1" % robot_id)
    last_log = cur.fetchone()
    if last_log:
        if last_log['content'] == log:
            return
    insert_sql = "insert jl_quant_robot_log(platform,uid,qrobot_id,content,type) values ('%s',%d,%d,'%s',%d)" % (
        platform, uid, robot_id, log, 2)
    cur.execute(insert_sql)
    conn.commit()
    cur.close()
    conn.close()


# 插入收益日志
def insertRevenueLog(platform, robot_id, pid, uid, market, stock, money, revenue):
    conn = Conn()
    cur = conn.cursor()
    insert_sql = "insert jl_quant_robot_revenue(platform,qrobot_id,pid,uid,market,stock,money,revenue,deal_status,type) values ('%s',%d,'%s',%d,'%s','%s','%s','%s',%d,%d)" % (
        platform,
        robot_id, pid, uid, market, stock, money, revenue, 0,2)
    # print(insert_sql)
    cur.execute(insert_sql)
    conn.commit()
    cur.close()
    conn.close()


# 插入订单
def insertOrder(platform, uid, order_id, robot_id, side, market, stock, money, deal_money, deal_amount, price, is_first,
                uuid):
    conn = Conn()
    cur = conn.cursor()
    insert_sql = "insert jl_quant_robot_order(platform,uid,qrobot_id,side,market,stock,money,deal_money,deal_amount,price,order_status,is_first,pid,order_id,type) values ('%s',%d,%d,%d,'%s','%s','%s','%s','%s','%s',%d,%d,'%s','%s',%d)" % (
        platform, uid, robot_id, side, market, stock, money, deal_money, deal_amount, price, 1, is_first,
        uuid, order_id, 2)
    # print(insert_sql)
    cur.execute(insert_sql)
    conn.commit()


def getRobotConfig(robot_id):
    conn = Conn()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * from jl_quant_robot where status = 1 and type =2 and id = %d" % robot_id)
    robot = cur.fetchone()
    return robot


# ccxt  初始化
def setExchange(api_info):
    ret = {}

    exchange_id = api_info['platform']
    api_key = api_info['api_key']
    secret_key = api_info['secret_key']
    passphrase = api_info['passphrase']

    try:
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class({
            'apiKey': api_key,
            'secret': secret_key,
            'password': passphrase,
            'timeout': 30000,
            'enableRateLimit': True,
            'rateLimit': 3000
        })
        ret['code'] = 1
        ret['data'] = exchange
        ret['msg'] = 'success'
        return ret

    except Exception as e:
        print(e)
        ret['code'] = 0
        ret['data'] = {}
        ret['msg'] = str(e)
        return ret


# 市价  side 1 4  买入 2 3 卖出  direction 1 3 多  2  4  空
def order(robot_id, side, exchange, market, amount, direction):
    global order_info
    ret = {}
    pending_order = {}
    if robot_id in pending_order:
        if pending_order[robot_id] == 1:
            ret['code'] = 2
            ret['data'] = {}
            ret['msg'] = 'wait pending order,robot:' + str(robot_id)

            return ret
        else:
            pending_order[robot_id] = 1
    else:
        pending_order[robot_id] = 1

    try:
        exchange.load_markets()

        if side == 1:
            side_type = 'buy'
        elif side == 2:
            side_type = 'sell'

        if direction == 1:
            pos_side = 'long'
        elif direction == 2:
            pos_side = 'short'

        orderInfo = exchange.privatePostTradeOrder({
            'instId': market,
            'tdMode': 'cross',
            'side': side_type,
            'posSide': pos_side,
            'ordType': 'market',
            'sz': int(amount)
        })

        if int(orderInfo['code']) == 0:

            order_info = {}
            order_info['order_id'] = orderInfo['data'][0]['ordId']  # 订单id
            time.sleep(1)  # 延迟1秒等交易完成

            order_log = getOrderInfo(exchange, market, order_info['order_id'])

            errorNum = 0
            while order_log['code'] == 1 and order_log['data'][0]['state'] != 'filled':
                time.sleep(0.5)
                order_log = exchange.getOrderInfo(exchange, market, order_info['order_id'])

                errorNum += 1

                # if errorNum >= 5:
                #     print("5次查询订单失败，默认机器人下单失败，关闭机器人:%d" % robot_id)
                #     break
            # print(order_log)
            if order_log['code'] == 1:
                order_info['deal_money'] = order_log['data'][0]['sz']  # 委托数量张数
                order_info['deal_price'] = order_log['data'][0]['px']  # 委托价格
                order_info['trade_avg_price'] = order_log['data'][0]['avgPx']  # 成交均价
                order_info['trade_volume'] = order_log['data'][0]['accFillSz']  # 成交量（张）
                order_info['order_status'] = order_log['data'][0][
                    'state']  # 订单状态	canceled：撤单成功 、 live：等待成交 、 partially_filled：部分成交、filled：完全成交
                order_info['deal_fee'] = order_log['data'][0]['fee']  # 总手续费
                order_info['profit'] = order_log['data'][0]['pnl']  # 订单总平仓盈亏（使用持仓均价计算，不包含仓位跨结算的已实现盈亏。）
                order_info['lever_rate'] = order_log['data'][0]['lever']  # 杠杆倍数

                ret['code'] = 1
                ret['data'] = order_info
                ret['msg'] = 'success'
                pending_order[robot_id] = 0
                return ret

            else:
                print("查询合约订单返回查询失败：%s" % order_log['msg'])
                ret['code'] = 2
                ret['data'] = {}
                ret['msg'] = '查询合约订单返回查询失败:' + str(order_log['msg'])
                return ret

        ret['code'] = 0
        ret['data'] = {}
        ret['msg'] = '下单失败'
        pending_order[robot_id] = 0
        return ret
    except Exception as e:
        print(e)
        ret['code'] = 0
        ret['data'] = {}
        ret['msg'] = str(e)
        pending_order[robot_id] = 0
        return ret


# 获取所有币种行情
def getAllTick(exchange, platform):
    if platform in platform_ticker_time:
        last_time = platform_ticker_time[platform]
        now_time = int(time.time())
        if now_time - last_time < 3:
            print('fetch', platform, 'ticker pass , wait next time')
            return

    try:
        print('fetch', platform, 'ticker')
        # 获得所有币种的行情
        ticker_data = exchange.publicGetMarketTickers({
            'instType': 'SWAP'
        })
        if isinstance(ticker_data, dict):
            for ticker_item in ticker_data['data']:
                if platform not in all_ticker:
                    all_ticker[platform] = {}
                all_ticker[platform][ticker_item['instId']] = ticker_item
            platform_ticker_time[platform] = int(time.time())
        else:
            print(ticker_data)
    except Exception as e:
        print(e)
        return None


# 获取币种价格
def getTick(exchange, platform, market):
    getAllTick(exchange, platform)
    try:
        print('fetch', platform, 'ticker : ', market)
        if platform in all_ticker:
            if market in all_ticker[platform]:
                print(platform, ' ', market, ' price:', all_ticker[platform][market]['last'])
                return all_ticker[platform][market]['last']
        else:
            print('fetch', platform, 'ticker ', market, ': error')
            return None
    except Exception as e:
        print(e)
        return None


# 获取账户杠杆
def getAccountLeverageInfo(exchange, market):
    ret = {}

    try:
        result = exchange.privateGetAccountLeverageInfo({
            'instId': market,
            'mgnMode': 'cross'
        })
        
        if float(result['data'][0]['lever']) != 10.00:
            ret['code'] = 2
            ret['data'] = {}
            ret['msg'] = '当前杠杆倍数%s' % result['data'][0]['lever']
            return ret

        ret['code'] = 1
        ret['data'] = result['data'][0]['lever']
        ret['msg'] = 'success'
        return ret

    except Exception as e:
        print(e)
        ret['code'] = 0
        ret['data'] = {}
        ret['msg'] = str(e)
        return ret


# 设置账户杠杆
def setAccountLeverage(exchange, market):
    ret = {}

    try:
        result = exchange.privatePostAccountSetLeverage({
            'instId': market,
            'mgnMode': 'cross',
            'lever': 10
        })

        if int(result['code']) != 0:
            ret['code'] = 0
            ret['data'] = {}
            ret['msg'] = '设置杠杆倍数失败'
            return ret

        ret['code'] = 1
        ret['data'] = result['data'][0]['lever']
        ret['msg'] = 'success'
        return ret

    except Exception as e:
        print(e)
        ret['code'] = 0
        ret['data'] = {}
        ret['msg'] = str(e)
        return ret

def getAccountConfig(exchange):
    ret = {}

    try:
        result = exchange.privateGetAccountConfig()

        if int(result['code']) != 0:
            ret['code'] = 0
            ret['data'] = {}
            ret['msg'] = '设置账户配置失败'
            return ret

        ret['code'] = 1
        ret['data'] = result['data'][0]['posMode']
        ret['msg'] = 'success'
        return ret

    except Exception as e:

        print(e)
        ret['code'] = 0
        ret['data'] = {}
        ret['msg'] = str(e)
        return ret

def setMode(exchange):
    ret = {}

    try:
        result = exchange.privatePostAccountSetPositionMode({
            'posMode': 'long_short_mode',
        })

        if int(result['code']) != 0:
            ret['code'] = 0
            ret['data'] = {}
            ret['msg'] = '设置账户配置失败'
            return ret

        ret['code'] = 1
        ret['data'] = result['data'][0]['posMode']
        ret['msg'] = 'success'
        return ret

    except Exception as e:

        print(e)
        ret['code'] = 0
        ret['data'] = {}
        ret['msg'] = str(e)
        return ret

def verifyMode(exchange):
    ret = {}
    smode = getAccountConfig(exchange)

    if smode['code'] == 1:

        if smode['data'] == 'net_mode':
            setsmode = setMode(exchange)

            if setsmode['code'] == 0:
                ret['code'] = 0
                ret['data'] = {}
                ret['msg'] = '设置杠杆倍数失败1'
                return ret
            else:
                ret['code'] = 2
                ret['data'] = {}
                ret['msg'] = 'success'
                return ret
        else:
            ret['code'] = 0
            ret['data'] = {}
            ret['msg'] = '当前账户账户模式为long_short_mode'
            return ret
    else:
        ret['code'] = 0
        ret['data'] = {}
        ret['msg'] = '设置账户配置失败'
        return ret
        

# 获取订单信息
def getOrderInfo(exchange, market, order_id):
    ret = {}

    try:
        result = exchange.privateGetTradeOrder({
            'instId': market,
            'ordId': order_id
        })

        if int(result['code']) != 0:
            ret['code'] = 0
            ret['data'] = {}
            ret['msg'] = '获取订单' + order_id + '信息失败'
            return ret

        ret['code'] = 1
        ret['data'] = result['data']
        ret['msg'] = 'success'
        return ret

    except Exception as e:

        print(e)
        ret['code'] = 0
        ret['data'] = {}
        ret['msg'] = str(e)
        return ret


def verifyLeverage(exchange, market):
    ret = {}
    leveinfo = getAccountLeverageInfo(exchange, market)

    if leveinfo['code'] == 2:
        setLevelInfo = setAccountLeverage(exchange, market)

        if setLevelInfo['code'] == 0:
            ret['code'] = 0
            ret['data'] = {}
            ret['msg'] = '设置杠杆倍数失败1'
            return ret
        else:
            ret['code'] = 2
            ret['data'] = 10
            ret['msg'] = 'success'
            return ret
    elif leveinfo['code'] == 0:
        ret['code'] = 0
        ret['data'] = {}
        ret['msg'] = '设置杠杆倍数失败2'
        return ret
    else:
        ret['code'] = 1
        ret['data'] = leveinfo['data']
        ret['msg'] = 'success'
        return ret

    # 获取历史订单记录


def getOrderInfoHistory(exchange, market):
    ret = {}

    try:
        result = exchange.privateGetTradeOrdersHistory({
            'instId': market,
            'instType': 'SWAP'
        })

        if int(result['code']) != 0:
            ret['code'] = 0
            ret['data'] = {}
            ret['msg'] = '获取订单' + market + '信息失败'
            return ret

        ret['code'] = 1
        ret['data'] = result['data']
        ret['msg'] = 'success'
        return ret

    except Exception as e:

        print(e)
        ret['code'] = 0
        ret['data'] = {}
        ret['msg'] = str(e)
        return ret


# 获取账户余额
def getAccountBalance(exchange):
    ret = {}
    accout = {}
    try:
        result = exchange.privateGetAccountBalance({
            'ccy': 'USDT',
        })
        # print(result)
        if int(result['code']) != 0:
            ret['code'] = 0
            ret['data'] = {}
            ret['msg'] = '获取信息失败'
            return ret

        ret['code'] = 1
        ret['data'] = result['data'][0]['details'][0]['cashBal']
        ret['msg'] = 'success'
        return ret

    except Exception as e:

        print(e)
        ret['code'] = 0
        ret['data'] = {}
        ret['msg'] = str(e)
        return ret


def onTick(robot_id, market_info, api_info):
    robot_config = getRobotConfig(robot_id)  # 获取机器人参数详情
    
    if not robot_config:
        print('------robot is empty-------')
        return
    if robot_config is None:
        print('------robot is none-------')
        return
    print(robot_config)
    print('------onTick-------')

    stock_name = market_info['stock']
    money_name = market_info['money']
    market = market_info['market']  # 合约交易对

    robot_id = robot_config['id']  # 机器人id
    platform = robot_config['platform']  # okex
    uid = robot_config['uid']
    is_clean = int(robot_config['is_clean'])  # 是否平仓

    if robot_id in thread_alive:
        if thread_alive[robot_id] == 1:
            print('wait pending thread,robot:' + str(robot_id))
            return
        else:
            thread_alive[robot_id] = 1
    else:
        thread_alive[robot_id] = 1

    getexchange = setExchange(api_info)

    if getexchange['code'] == 1:
        exchange = getexchange['data']
    else:
        thread_alive[robot_id] = 0
        print('初始化ccxt:exchange失败,robot:' + str(robot_id))
        return
    
    #设置下单杠杆倍数
    changeLevel = verifyLeverage(exchange, market)

    if changeLevel['code'] == 2:
        print('检测到okex交易所:%s 杠杆倍数不是10，重置成功' % market)
    elif changeLevel['code'] == 0:
        thread_alive[robot_id] = 0
        print('初始化杠杆倍数失败,robot:' + str(robot_id))
        return
    
    changeMode = verifyMode(exchange)
    if changeLevel['code'] == 2:
        print('检测到okex交易所:%s 交易模式不是多空，重置成功' % market)
    elif changeLevel['code'] == 0:
        thread_alive[robot_id] = 0
        print('交易模式设置失败,robot:' + str(robot_id))
        return
    
    
    
    tick_price = float(getTick(exchange, platform, market))

    print('*********tick_price******************')
    print('tick_price:%f' % tick_price)
    if tick_price is None:
        thread_alive[robot_id] = 0
        return

    direction = int(robot_config['direction'])  # 1 做多 2 做空
    limit_price = float(robot_config['price'])  # 限价价格
    first_order_value = float(robot_config['first_order_value'])  # 张数
    max_order_count = int(robot_config['max_order_count'])  # 最大做单次数
    stop_profit_rate = float(robot_config['stop_profit_rate'])  # 止盈比例
    stop_profit_callback_rate = float(robot_config['stop_profit_callback_rate'])  # 止盈回调
    cover_ratearr = json.loads(robot_config['cover_rate'])  # 补仓跌幅
    cover_callback_rate = float(robot_config['cover_callback_rate'])  # 补仓回调
    values_str = robot_config['values_str']  # 机器人运行中各种参数
    c_type = int(robot_config['c_type'])  # 1 等额 2倍额 3 差额
    
    sl_trigger_price = float(robot_config['sl_trigger_price'])
    
    if values_str:
        values_dict = json.loads(values_str)
        print(values_dict)

        base_price = float(values_dict['base_price'])
        up_price = float(values_dict['up_price'])
        down_price = float(values_dict['down_price'])
        trend_side = int(values_dict['trend_side'])
        deal_money = float(values_dict['deal_money'])

        # 做多：收益 =（平仓价 - 开仓价）*面值 * 张数 =（平仓价 - 开仓价）*数量
        # 做空：收益 =（开仓价 - 平仓价）*面值 * 张数 =（开仓价 - 平仓价）*数量
        if direction == 1:
            revenue = float(market_info['contract_size']) * float(values_dict['deal_amount']) * (
                        float(tick_price) - base_price)
        else:
            revenue = float(market_info['contract_size']) * float(values_dict['deal_amount']) * (
                        base_price - float(tick_price))

        updateRevenue(robot_id, revenue)
        
        if revenue < 0:
            
            zhisun = abs(revenue) * 100 / deal_money
            
            if zhisun >= sl_trigger_price:
                insertLog(platform, robot_id, uid, u"止损清仓卖出指令 ,当前价格 %s" % tick_price)

                if direction == 1:
                    sideclean = 2
                else:
                    sideclean = 1
    
                rst = order(robot_id, sideclean, exchange, market, int(values_dict['deal_amount']), direction)
    
                if rst['code'] == 1:
                    cleanFinish(robot_id)
    
                    order_id = rst['data']['order_id']  # 订单id
                    deal_amount = rst['data']['deal_money']  # 委托数量张数
    
                    # 计算初始保证金  开仓保证金=面值*张数*最新标记价格／杠杆
                    deal_money = float(deal_amount) * float(market_info['contract_size']) * float(
                        rst['data']['trade_avg_price']) / float(
                        rst['data']['lever_rate'])
    
                    deal_fee = rst['data']['deal_fee']  # 手续费
                    price = float(rst['data']['trade_avg_price'])  # 成交均价
                    side = 1
    
                    insertOrder(platform, uid, order_id, robot_id, side, market, stock_name,
                                money_name, deal_money, deal_amount, price, 2, values_dict['pid'])
    
                    revenue = float(rst['data']['profit'])  # 收益
    
                    insertRevenueLog(platform, robot_id, values_dict['pid'], uid, market, stock_name, money_name, revenue)
    
                    updateValues(robot_id, '')
                    updateRevenue(robot_id, 0)
                    updateMsg(robot_id, u'止损清仓卖出成功')
                    insertLog(platform, robot_id, uid, u"止损清仓卖出：成交总价 %s %s ,成交均价 %s %s,成交数量（张） %s %s,手续费 %s" % (
                        deal_money, money_name, price, money_name, deal_amount, stock_name, deal_fee))
    
                    # 关闭机器人
                    disableRobot(robot_id)
                    insertLog(platform, robot_id, uid, u"量化机器人已经关闭")
    
                    thread_alive[robot_id] = 0
                    return
                else:
                    # 关闭机器人
                    disableRobot(robot_id)
                    insertLog(platform, robot_id, uid, u",量化机器人已经关闭")
    
                    updateMsg(robot_id, u'止损清仓卖出失败' + rst['msg'])
                    insertLog(platform, robot_id, uid, u'止损清仓卖出失败' + rst['msg'])
                    thread_alive[robot_id] = 0
                    return

        # 清仓卖出
        if is_clean == 1:
            insertLog(platform, robot_id, uid, u"收到清仓卖出指令 ,当前价格 %s" % tick_price)

            if direction == 1:
                sideclean = 2
            else:
                sideclean = 1

            rst = order(robot_id, sideclean, exchange, market, values_dict['deal_amount'], direction)

            print("平仓：", rst)
            if rst['code'] == 1:
                cleanFinish(robot_id)

                order_id = rst['data']['order_id']  # 订单id
                deal_amount = rst['data']['deal_money']  # 委托数量张数

                # 计算初始保证金  开仓保证金=面值*张数*最新标记价格／杠杆
                deal_money = float(deal_amount) * float(market_info['contract_size']) * float(
                    rst['data']['trade_avg_price']) / float(
                    rst['data']['lever_rate'])

                deal_fee = rst['data']['deal_fee']  # 手续费
                price = float(rst['data']['trade_avg_price'])  # 成交均价
                side = 1

                insertOrder(platform, uid, order_id, robot_id, side, market, stock_name,
                            money_name, deal_money, deal_amount, price, 2, values_dict['pid'])

                revenue = float(rst['data']['profit'])  # 收益

                insertRevenueLog(platform, robot_id, values_dict['pid'], uid, market, stock_name, money_name, revenue)

                updateValues(robot_id, '')
                updateRevenue(robot_id, 0)
                updateMsg(robot_id, u'清仓卖出成功')
                insertLog(platform, robot_id, uid, u"清仓卖出：成交总价 %s %s ,成交均价 %s %s,成交数量（张） %s %s,手续费 %s" % (
                    deal_money, money_name, price, money_name, deal_amount, stock_name, deal_fee))

                # 关闭机器人
                disableRobot(robot_id)
                insertLog(platform, robot_id, uid, u"量化机器人已经关闭")

                thread_alive[robot_id] = 0
                return
            else:
                # 关闭机器人
                disableRobot(robot_id)
                insertLog(platform, robot_id, uid, u",量化机器人已经关闭")

                updateMsg(robot_id, u'清仓卖出失败' + rst['msg'])
                insertLog(platform, robot_id, uid, u'清仓卖出失败' + rst['msg'])
                thread_alive[robot_id] = 0
                return
        # 判断趋势

        print('开仓均价:%f' % base_price)
        
        print('当前收益率：',revenue* 100 / deal_money)
        # 收益率=收益/开仓所需保证金
        if tick_price > base_price:
            # 做多
            if direction == 1:
                if trend_side == 0 or trend_side == 2:
                    # up_num = tick_price - base_price
                    # up_rate = up_num * 100 / base_price
                    up_rate = revenue * 100 / deal_money

                    print('止盈率:%f' % up_rate)
                    print('条件止盈率:%f' % stop_profit_rate)
                    if up_rate >= stop_profit_rate:
                        # 上涨到止盈率
                        values_dict['trend_side'] = 1
                        values_dict['up_price'] = tick_price
                        updateValues(robot_id, json.dumps(values_dict))
                        insertLog(platform, robot_id, uid, u"达到止盈率 %s ,当前上涨价格 %s" %
                                  (up_rate, tick_price))
                if trend_side == 1:
                    # 判断是否达到止盈回调
                    if tick_price > up_price:
                        # 继续涨了
                        values_dict['up_price'] = tick_price
                        updateValues(robot_id, json.dumps(values_dict))
                        insertLog(platform, robot_id, uid, u"达到止盈率后继续上涨 ,当前上涨价格 %s" %
                                  (tick_price))
                    else:
                        down_num = up_price - tick_price
                        down_rate = float(market_info['contract_size']) * float(
                            values_dict['deal_amount']) * down_num*100 / deal_money
                            
                        print('止盈回调率:',down_rate)
                        if down_rate >= stop_profit_callback_rate:
                            # 达到止盈回调了，卖出所有deal_amount
                            # updateValues(robot_id,'')
                            insertLog(platform, robot_id, uid, u"达到止盈回调率 %s ,当前回调价格 %s" %
                                      (down_rate, tick_price))

                            rst = order(robot_id, 2, exchange, market, values_dict['deal_amount'], direction)

                            print(rst)
                            if rst['code'] == 1:

                                order_id = rst['data']['order_id']  # 订单id
                                deal_amount = rst['data']['deal_money']  # 委托数量张数

                                # 计算初始保证金  开仓保证金=面值*张数*最新标记价格／杠杆
                                deal_money = float(deal_amount) * float(market_info['contract_size']) * float(
                                    rst['data']['trade_avg_price']) / float(
                                    rst['data']['lever_rate'])

                                deal_fee = rst['data']['deal_fee']  # 手续费
                                price = float(rst['data']['trade_avg_price'])  # 成交均价

                                side = 1
                                insertOrder(platform, uid, order_id, robot_id, side, market, stock_name,
                                            money_name, deal_money, deal_amount, price, 2, values_dict['pid'])

                                revenue = float(rst['data']['profit'])  # 收益

                                insertRevenueLog(
                                    platform, robot_id, values_dict['pid'], uid, market, stock_name, money_name,
                                    revenue)
                                updateValues(robot_id, '')
                                updateRevenue(robot_id, 0)
                                updateMsg(robot_id, u'卖出成功')
                                insertLog(platform, robot_id, uid, u"开多卖出：成交总价 %s %s ,成交均价 %s %s,成交数量(张) %s %s,手续费 %s" % (
                                    deal_money, money_name, price, money_name, deal_amount, stock_name, deal_fee))
                                # 关闭机器人
                                disableRobot(robot_id)
                                insertLog(platform, robot_id,
                                          uid, u"量化机器人已经关闭")

                            else:
                                if values_dict['fail_count'] < 3:

                                    values_dict['fail_count'] = values_dict['fail_count'] + 1
                                    updateValues(robot_id, json.dumps(values_dict))
                                    updateMsg(robot_id, u'平多卖出失败' + rst['msg'])
                                    insertLog(platform, robot_id, uid,
                                              u'平多卖出失败' + rst['msg'])
                                else:
                                    disableRobot(robot_id)
                                    updateMsg(robot_id, u'多次卖出失败，机器人停止运行')
            else:
                if values_dict['order_finish'] == 1:
                    # 达到最大做单次数后，不能再补仓了
                    thread_alive[robot_id] = 0
                    return
                if trend_side == 0 or trend_side == 1:
                    # down_num = base_price - tick_price
                    # down_rate = down_num * 100 / base_price

                    down_rate = abs(revenue)* 100 / deal_money  # 价格下降  做多  为负数
                    cover_rate = float(cover_ratearr[str(values_dict['order_count'])])
                    
                    print('做空下跌率：',down_rate)
                    if down_rate >= cover_rate:
                        # 下跌到补仓线
                        values_dict['trend_side'] = 2
                        values_dict['down_price'] = tick_price
                        updateValues(robot_id, json.dumps(values_dict))
                        insertLog(platform, robot_id, uid, u"上涨到补仓线 %s ,当前上涨价格 %s" %
                                  (down_rate, tick_price))
                if trend_side == 2:
                    # 判断是否达到补仓回调
                    if tick_price > down_price:
                        # 继续涨了
                        values_dict['down_price'] = tick_price
                        updateValues(robot_id, json.dumps(values_dict))
                        insertLog(platform, robot_id, uid, u"达到补仓线后继续上涨 ,当前上涨价格 %s" %
                                  (tick_price))
                    else:
                        up_num = down_price - tick_price

                        up_rate = float(market_info['contract_size']) * float(
                            values_dict['deal_amount']) * up_num / deal_money
                            
                        up_rate = up_rate*100
                        
                        print('做空补仓回调率：',up_rate)
                        if up_rate >= cover_callback_rate:
                            # 达到补仓回调了，补仓
                            insertLog(platform, robot_id, uid, u"达到补仓回调率 %s ,当前回调价格 %s" %
                                      (up_rate, tick_price))
                            if c_type == 2:
                                t_num = first_order_value * math.pow(2, values_dict['order_count'])
                            elif c_type == 1:
                                t_num = first_order_value
                            else:
                                t_num = first_order_value * (values_dict['order_count'] + 1)

                            rst = order(robot_id, 2, exchange, market, t_num, direction)

                            if rst['code'] == 1:

                                order_id = rst['data']['order_id']  # 订单id
                                deal_amount = rst['data']['deal_money']  # 委托数量张数

                                # 计算初始保证金  开仓保证金=面值*张数*最新标记价格／杠杆
                                deal_money = float(deal_amount) * float(market_info['contract_size']) * float(
                                    rst['data']['trade_avg_price']) / float(
                                    rst['data']['lever_rate'])

                                deal_fee = rst['data']['deal_fee']  # 手续费
                                price = float(rst['data']['trade_avg_price'])  # 成交均价

                                side = 2

                                insertOrder(platform, uid, order_id, robot_id, side, market, stock_name,
                                            money_name, deal_money, deal_amount, price, 0, values_dict['pid'])
                                values_dict['order_count'] = values_dict['order_count'] + 1
                                values_dict['trend_side'] = 0
                                values_dict['deal_amount'] = int(
                                    values_dict['deal_amount']) + int(deal_amount)
                                values_dict['first_order_price'] = float(
                                    values_dict['first_order_price']) + float(price)
                                values_dict['deal_money'] = float(
                                    values_dict['deal_money']) + float(deal_money)
                                values_dict['base_price'] = float(
                                    values_dict['first_order_price'] / values_dict['order_count'])
                                # 达到最大做单数量后，标记finish，只能等盈利
                                if values_dict['order_count'] >= max_order_count:
                                    # 只能等盈利
                                    values_dict['order_finish'] = 1
                                    insertLog(platform, robot_id, uid, u"达到最大做单数量次数：单数 %s " %
                                              values_dict['order_count'])
                                updateValues(robot_id, json.dumps(values_dict))

                                updateMsg(robot_id, u'补仓成功')
                                insertLog(platform, robot_id, uid,
                                          u"开空补仓成功：单数 %s , 成交总价 %s %s ,成交均价 %s %s,成交数量(张) %s %s,手续费 %s" % (
                                              values_dict['order_count'], deal_money, money_name, price, money_name,
                                              deal_amount,
                                              stock_name, deal_fee))
                                insertLog(platform, robot_id, uid, u"基准价调整为: %s " %
                                          values_dict['base_price'])
                            else:
                                disableRobot(robot_id)
                                insertLog(platform, robot_id, uid, u"补仓失败，量化机器人已经关闭")
                                updateMsg(robot_id, u'补仓失败 : ' + rst['msg'])
                                insertLog(platform, robot_id, uid,
                                          u'补仓失败 : ' + rst['msg'])

        if tick_price < base_price:
            # 做空
            if direction == 2:
                if trend_side == 0 or trend_side == 2:
                    # up_num = tick_price - base_price
                    # up_rate = up_num * 100 / base_price
                    up_rate = revenue * 100 / deal_money

                    print('做空止盈率:%f' % up_rate)
                    print('做空条件止盈率:%f' % stop_profit_rate)
                    if up_rate >= stop_profit_rate:
                        # 上涨到止盈率
                        values_dict['trend_side'] = 1
                        values_dict['up_price'] = tick_price
                        updateValues(robot_id, json.dumps(values_dict))
                        insertLog(platform, robot_id, uid, u"达到止盈率 %s ,当前下跌价格 %s" %
                                  (up_rate, tick_price))
                if trend_side == 1:
                    # 判断是否达到止盈回调
                    if tick_price < up_price:
                        # 暴跌
                        values_dict['up_price'] = tick_price
                        updateValues(robot_id, json.dumps(values_dict))
                        insertLog(platform, robot_id, uid, u"达到止盈率后继续下跌 ,当前下跌价格 %s" %
                                  (tick_price))
                    else:
                        down_num =  tick_price - up_price
                        down_rate = float(market_info['contract_size']) * float(
                            values_dict['deal_amount']) * down_num *100/ deal_money
                        
                        print('做空止盈回调率：',down_rate)
                        if down_rate >= stop_profit_callback_rate:
                            # 达到止盈回调了，卖出所有deal_amount
                            # updateValues(robot_id,'')
                            insertLog(platform, robot_id, uid, u"达到止盈回调率 %s ,当前回调价格 %s" %
                                      (down_rate, tick_price))

                            rst = order(robot_id, 1, exchange, market, values_dict['deal_amount'], direction)

                            # print(rst)
                            if rst['code'] == 1:

                                order_id = rst['data']['order_id']  # 订单id
                                deal_amount = rst['data']['deal_money']  # 委托数量张数

                                # 计算初始保证金  开仓保证金=面值*张数*最新标记价格／杠杆
                                deal_money = float(deal_amount) * float(market_info['contract_size']) * float(
                                    rst['data']['trade_avg_price']) / float(
                                    rst['data']['lever_rate'])

                                deal_fee = rst['data']['deal_fee']  # 手续费
                                price = float(rst['data']['trade_avg_price'])  # 成交均价

                                side = 1
                                insertOrder(platform, uid, order_id, robot_id, side, market, stock_name,
                                            money_name, deal_money, deal_amount, price, 2, values_dict['pid'])

                                revenue = float(rst['data']['profit'])  # 收益

                                insertRevenueLog(
                                    platform, robot_id, values_dict['pid'], uid, market, stock_name, money_name,
                                    revenue)
                                updateValues(robot_id, '')
                                updateRevenue(robot_id, 0)
                                updateMsg(robot_id, u'卖出成功')
                                insertLog(platform, robot_id, uid,
                                          u"开空卖出：成交总价 %s %s ,成交均价 %s %s,成交数量(张) %s %s,手续费 %s" % (
                                              deal_money, money_name, price, money_name, deal_amount,
                                              stock_name, deal_fee))
                                # 关闭机器人
                                disableRobot(robot_id)
                                insertLog(platform, robot_id,
                                          uid, u"量化机器人已经关闭")

                            else:
                                if values_dict['fail_count'] < 3:

                                    values_dict['fail_count'] = values_dict['fail_count'] + 1
                                    updateValues(robot_id, json.dumps(values_dict))
                                    updateMsg(robot_id, u'平空卖出失败' + rst['msg'])
                                    insertLog(platform, robot_id, uid,
                                              u'平空卖出失败' + rst['msg'])
                                else:
                                    disableRobot(robot_id)
                                    updateMsg(robot_id, u'多次卖出失败，机器人停止运行')
            else:
                if values_dict['order_finish'] == 1:
                    # 达到最大做单次数后，不能再补仓了
                    thread_alive[robot_id] = 0
                    return
                if trend_side == 0 or trend_side == 1:
                    # down_num = base_price - tick_price
                    # down_rate = down_num * 100 / base_price

                    down_rate = abs(revenue)* 100 / deal_money  # 价格下降  做多  为负数
                    cover_rate = float(cover_ratearr[str(values_dict['order_count'])])
                    
                    print('做多下跌率：',down_rate)
                    if down_rate >= cover_rate:
                        # 下跌到补仓线
                        values_dict['trend_side'] = 2
                        values_dict['down_price'] = tick_price
                        updateValues(robot_id, json.dumps(values_dict))
                        insertLog(platform, robot_id, uid, u"下跌到补仓线 %s ,当前下跌价格 %s" %
                                  (down_rate, tick_price))
                if trend_side == 2:
                    # 判断是否达到补仓回调
                    if tick_price < down_price:
                        # 继续跌了
                        values_dict['down_price'] = tick_price
                        updateValues(robot_id, json.dumps(values_dict))
                        insertLog(platform, robot_id, uid, u"达到补仓线后继续下跌 ,当前下跌价格 %s" %
                                  (tick_price))
                    else:
                        up_num = tick_price - down_price

                        up_rate = float(market_info['contract_size']) * float(
                            values_dict['deal_amount']) * up_num / deal_money
                        
                        up_rate = up_rate*100
                        print('做多补仓回调：',up_rate)
                        
                        if up_rate >= cover_callback_rate:
                            # 达到补仓回调了，补仓
                            insertLog(platform, robot_id, uid, u"达到补仓回调率 %s ,当前回调价格 %s" %
                                      (up_rate, tick_price))
                            if c_type == 2:
                                t_num = first_order_value * math.pow(2, values_dict['order_count'])
                            elif c_type == 1:
                                t_num = first_order_value
                            else:
                                t_num = first_order_value * (values_dict['order_count'] + 1)

                            rst = order(robot_id, 1, exchange, market, t_num, direction)

                            if rst['code'] == 1:

                                order_id = rst['data']['order_id']  # 订单id
                                deal_amount = rst['data']['deal_money']  # 委托数量张数

                                # 计算初始保证金  开仓保证金=面值*张数*最新标记价格／杠杆
                                deal_money = float(deal_amount) * float(market_info['contract_size']) * float(
                                    rst['data']['trade_avg_price']) / float(
                                    rst['data']['lever_rate'])

                                deal_fee = rst['data']['deal_fee']  # 手续费
                                price = float(rst['data']['trade_avg_price'])  # 成交均价

                                side = 2

                                insertOrder(platform, uid, order_id, robot_id, side, market, stock_name,
                                            money_name, deal_money, deal_amount, price, 0, values_dict['pid'])
                                values_dict['order_count'] = values_dict['order_count'] + 1
                                values_dict['trend_side'] = 0
                                values_dict['deal_amount'] = int(
                                    values_dict['deal_amount']) + int(deal_amount)
                                values_dict['first_order_price'] = float(
                                    values_dict['first_order_price']) + float(price)
                                values_dict['deal_money'] = float(
                                    values_dict['deal_money']) + float(deal_money)
                                values_dict['base_price'] = float(
                                    values_dict['first_order_price'] / values_dict['order_count'])
                                # 达到最大做单数量后，标记finish，只能等盈利
                                if values_dict['order_count'] >= max_order_count:
                                    # 只能等盈利
                                    values_dict['order_finish'] = 1
                                    insertLog(platform, robot_id, uid, u"达到最大做单数量次数：单数 %s " %
                                              values_dict['order_count'])
                                updateValues(robot_id, json.dumps(values_dict))

                                updateMsg(robot_id, u'补仓成功')
                                insertLog(platform, robot_id, uid,
                                          u"开多补仓成功：单数 %s , 成交总价 %s %s ,成交均价 %s %s,成交数量(张) %s %s,手续费 %s" % (
                                              values_dict['order_count'], deal_money, money_name, price,
                                              money_name,
                                              deal_amount,
                                              stock_name, deal_fee))
                                insertLog(platform, robot_id, uid, u"基准价调整为: %s " %
                                          values_dict['base_price'])
                            else:
                                disableRobot(robot_id)
                                insertLog(platform, robot_id, uid, u"补仓失败，量化机器人已经关闭")
                                updateMsg(robot_id, u'补仓失败 : ' + rst['msg'])
                                insertLog(platform, robot_id, uid,
                                          u'补仓失败 : ' + rst['msg'])
    else:

        if is_clean == 1:
            cleanFinish(robot_id)
            updateValues(robot_id, '')
            updateRevenue(robot_id, 0)
            thread_alive[robot_id] = 0
            return
        # 新启动的
        # 开始下单 收益率=收益/开仓所需保证金
        # 做多  当前价格 > 买入价
        # 做空  当前价  < 买入价

        if direction == 1:
            if tick_price > limit_price:
                print('做多：tick_price:%f --- limit_price:%f' % (tick_price,limit_price))
                thread_alive[robot_id] = 0
                return
        else:
            if tick_price < limit_price:
                print('做空：tick_price:%f --- limit_price:%f' % (tick_price, limit_price))
                thread_alive[robot_id] = 0
                return
        rst = order(robot_id, direction, exchange, market, first_order_value, direction)

        # print('首单开单：', rst)

        if rst['code'] == 1:
            order_id = rst['data']['order_id']  # 订单id
            deal_amount = rst['data']['deal_money']  # 委托数量张数

            # 计算初始保证金  开仓保证金=面值*张数*最新标记价格／杠杆
            deal_money = float(deal_amount) * float(market_info['contract_size']) *float(rst['data']['trade_avg_price']) / float(
                rst['data']['lever_rate'])

            deal_fee = rst['data']['deal_fee']  # 手续费
            price = float(rst['data']['trade_avg_price'])  # 成交均价

            side = 2
            pid = str(uuid.uuid4())

            insertOrder(platform, uid, order_id, robot_id, side, market, stock_name,
                        money_name, deal_money, deal_amount, price, 1, pid)
            values_dict = {'first_order_price': price, 'base_price': price, 'up_price': 0, 'down_price': 0,
                           'trend_side': 0,
                           'order_count': 1, 'deal_amount': deal_amount, 'deal_money': deal_money, 'order_finish': 0,
                           'pid': pid, 'fail_count': 0}
            updateValues(robot_id, json.dumps(values_dict))
            updateMsg(robot_id, u'下单成功')

            insertLog(platform, robot_id, uid, u"首单开单：成交总价 %s %s ,成交均价 %s %s,成交数量（张） %s %s,手续费 %s" % (
                deal_money, money_name, price, money_name, deal_amount, stock_name, deal_fee))
        else:
            disableRobot(robot_id)
            updateMsg(robot_id, u'首单开单失败 : ' + rst['msg'])
            insertLog(platform, robot_id, uid, u'器人已经关闭-首单开单失败 : ' + rst['msg'])
    # return
    thread_alive[robot_id] = 0  # 修改线程运行状态


# 读取所有的策略配置
def loadStrategyConfig(cur):
    # read db
    markets_count = cur.execute(
        "select id,platform,market,market_name,type,stock,money,contract_size from jl_spot_market where status = 1")
    # print('db have %d market' % markets_count)
    markets = cur.fetchall()
    # print(markets)
    market_list = {}
    for market in markets:
        market_list[market['id']] = market
    # print(market_list)
    # read api key
    api_count = cur.execute(
        "select id,uid,platform,api_key,secret_key,passphrase from jl_third_api where status = 1")
    # print('db have %d api' % api_count)
    apis = cur.fetchall()
    # print(apis)
    api_list = {}
    for api in apis:
        api_list["%s-%s" % (api['platform'], api['uid'])] = api
    # print(api_list)
    cur.execute('SELECT * from jl_quant_robot where status = 1 and type = 2')
    robots = cur.fetchall()
    if robots:
        for robot in robots:
            market_id = robot['market_id']
            platform = robot['platform']
            uid = robot['uid']
            robot_id = robot['id']
            if market_id in market_list:
                market_info = market_list[market_id]
            else:
                disableRobot(robot_id)
                updateMsg(robot_id, 'market %s not found' % market_id)
                insertLog(platform,
                          robot_id, uid, 'market %s  not found , stopped...' % market_id)
                continue
            if "%s-%s" % (platform, uid) in api_list:
                api_info = api_list["%s-%s" % (platform, uid)]
            else:
                disableRobot(robot_id)
                updateMsg(robot_id, '%s api not found' % platform)
                insertLog(platform, robot_id, uid,
                          '%s api not found , stopped...' % platform)
                continue
            # print(robot)
            # print(market_info)
            # print(api_info)
            time.sleep(1)
            _thread.start_new_thread(
                onTick, (robot_id, market_info, api_info))
    else:
        print(u'no robot , wait ...')


if __name__ == '__main__':

    while True:
        try:
            conn = Conn()
            cur = conn.cursor(MySQLdb.cursors.DictCursor)
            loadStrategyConfig(cur)
            cur.close()
            conn.close()
            time.sleep(5)
        except Exception as e:
            print(Exception, ':', e)
            time.sleep(10)
