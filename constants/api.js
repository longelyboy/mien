export default {
  UPLOAD_ONE: 'api/user/upload/one', // 文件上传

  INIT_INFO: 'api/home/main/init', // 初始化信息
  CHECK_UPDATE: 'api/home/main/checkUpdate', // 更新信息

  BANNER: 'api/home/main/banner', // 首页Banner
  NOTICE_LISTS: 'api/home/notice/lists', // 公告文章列表

  TICKER_ALL: 'api/home/ticker/all', // 所有行情
  TICKER_LIST: 'api/home/ticker/lists', // 我的行情
  TICKER_ADD: 'api/home/ticker/add', // 添加行情
  TICKER_REMOVE: 'api/home/ticker/delete', // 移除行情
  TICKER_SORT: 'api/home/ticker/sort', // 行情排序

  SEND_VERIFICATION_CODE: 'api/user/verification_code/send', // 验证码
  REGISTER: 'api/user/public/register', // 注册
  LOGIN: 'api/user/public/login', // 登录
  CODE_LOGIN: 'api/user/public/vcode_login', // 验证码登录
  CHANGE_PWD: 'api/user/profile/changePassword', // 修改密码
  RESET_PWD: 'api/user/public/passwordReset', // 重置密码
  BIND_EMAIL: 'api/user/profile/bindingEmail', // 绑定邮箱
  BIND_PHONE: 'api/user/profile/bindingMobile', // 绑定手机
  USER_INFO: 'api/user/profile/userInfo', // 用户信息
  INVITATION_INFO: 'api/user/invitation/info', // 邀请信息
  INVITATION_LIST: 'api/user/invitation/getList', // 已邀请列表
  ADD_PAY_PWD: 'api/user/pay_pwd/addpwd', // 添加支付密码
  CHANGE_PAY_PWD: 'api/user/pay_pwd/uppwd', // 更新支付密码
  FORGET_PAY_PWD: 'api/user/pay_pwd/forgetpwd', // 找回支付密码
  INVITATION_LEVEL: 'api/user/invitation/changeUserLevel',
  INVITATION_LEVELLIST: 'api/user/invitation/levelList', // 好友数量

  USER_AUTH: 'api/user/user_auth/getAuthGrade', // 获取认证等级描述
  ADD_AUTH: 'api/user/user_auth/addauth', // 申请实名认证
  SHOW_AUTH: 'api/user/user_auth/showauth', // 查询实名认证详情

  OPEN_CHECK_GOOGLE: 'api/user/google/opencheck', // 开启前绑定Google二级验证
  CONFIRM_CHECK_GOOGLE: 'api/user/google/confirmCheck', // 确认开启Google二步验证
  CLOSE_CHECK_GOOGLE: 'api/user/google/closecheck', // 关闭Google二步验证

  API_ACCOUNT: 'api/third/account/accountInfo', // 查看对应平台的API账户
  API_ACCOUNT_EDIT: 'api/third/account/addAccount', // 设定(重新填写)API账户
  API_ACCOUNT_REMOVE: 'api/third/account/removeAccount', // 删除API账户
  API_ACCOUNT_BALANCE: 'api/third/account/accountBalance', // 查看对应平台的API账户币种余额
  API_ACCOUNT_BALANCE_SWAP: 'api/third/account/accountSwapBalance', // 查看对应平台的API账户币种余额

  MARKET_LIST: 'api/quant/robot/marketList', // 市场列表
  STRATEGY_LIST: 'api/quant/robot/strategy', // 策略列表
  ROBOT_LIST: 'api/quant/robot/robotList', // 机器人列表
  ROBOT_POSITION: 'api/quant/robot/robotpai', // 机器人列表
  ROBOT_CREATE: 'api/quant/robot/create', // 创建机一个量化机器人
  ROBOT_EDIT: 'api/quant/robot/edit', // 更新机器人参数
  ROBOT_DISABLE: 'api/quant/robot/disable', // 禁用机器人
  ROBOT_ENABLE: 'api/quant/robot/enable', // 启用机器人
  ROBOT_CLEAN: 'api/quant/robot/clean', // 清仓卖出
  ROBOT_LOG: 'api/quant/robot/log', // 机器人日志
  ROBOT_ORDER: 'api/quant/robot/order', // 机器人订单
  ROBOT_REVENUE: 'api/quant/robot/revenue', // 机器人收益账单
  ROBOT_PRICE: '/api/quant/robot/getLimitPrice', // 获取合约最高价和最低价
  ROBOT_STRATEGY: '/api/quant/robot/strategy', // 获取后台默认参数

  CDKEY_LIST: 'api/user/cdkey/list', // 激活码列表
  CDKEY_INPUT: 'api/user/cdkey/input', // 手工领取激活码
  CDKEY_BUY: 'api/user/cdkey/buy', // 购买激活码

  // 资产
  WALLET_LIST: 'api/wallet/cloud/lists',
  WALLET_DETAIL: 'api/wallet/account/info',
  Scorelog: 'api/wallet/account/scorelog',
  WALLET_WITHDRAW: '/api/wallet/account/transfer',
  WALLET_BILL: 'api/wallet/account/transactions',
  WALLET_ADDR: 'api/wallet/account/address',
  BALANCE_LOG: 'api/user/balance/log',
  BALANCE_TRANSFER: 'api/user/balance/transfer',
  ACCOUT_Game: 'api/wallet/account/game',
  GamelogList: '/api/wallet/account/gamelog',

  // 授权登录
  OPEN_AUTH_LOGIN: 'api/user/third/openAuthLogin',

  // 查询指定交易对当前价格行情
  PUBLIC_TICKER: 'api/trade/public/ticker',

  // 获取合约行情
  PUBLIC_TICKER_SWAP: 'api/trade/public/swapticker',

  // 购买套餐
  PACKAGE_LIST: 'api/user/package/list',
  PACKAGE_BUY: 'api/user/package/buy'
}
