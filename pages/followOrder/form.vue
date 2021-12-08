<template>
  <div>
    <van-nav-bar
      title="跟单设置"
      left-arrow
      @click-left="$router.back()"
    />
    <van-row class="item-hd" type="flex" justify="space-between" align="center">
      <van-col class="user">
        <van-row type="flex" align="center">
          <van-col><div class="head"><img src="@/assets/images/header.png"/></div></van-col>
          <van-col class="user">
            <div>DJ黑天鹅 <span class="sub">458人跟随</span></div>
            <div class="info van-ellipsis">简单重复简单重复简单重复简单重复简单重复简单重复</div>
          </van-col>
        </van-row>
      </van-col>
    </van-row>
    <van-cell-group>
      <van-cell title="跟单合约及杠杆倍数" value="所有合约" is-link />
      <van-cell title="跟单模式" value="所有合约" is-link />
      <van-cell title="跟单金额(USDT)"><van-stepper v-model="value" class="lang" step="0.0001" decimal-length="4" /></van-cell>
      <van-row class="tip" type="flex" justify="space-between">
        <van-col>限额：100.0000 ~ 10000.0000</van-col>
        <van-col>币币可用0.0000 USDT</van-col>
      </van-row>
    </van-cell-group>
    <div class="title">结束跟单设置</div>
    <van-cell-group>
      <van-cell title="止损超过(%)"><van-stepper v-model="value" step="1" /></van-cell>
      <van-cell title="盈利超过(%)"><van-stepper v-model="value" step="1" /></van-cell>
    </van-cell-group>
    <div class="tip2">
      <h3>跟单提醒</h3>
      <p>开始跟单后，系统将以您输入的跟单金额作为保证金跟随带人以相同仓位、方向、杠杆倍数下单，当带单人下单金额小于此金额时，系统会按跟单人金额进行下单</p>
    </div>
    <div class="ft-btn">
      <van-button type="primary" block>开始跟单</van-button>
    </div>
  </div>
</template>

<script>
import { Stepper } from 'vant'
export default {
  components: {
    [Stepper.name]: Stepper
  }
}
</script>

<style lang="less" scoped>
.item-hd {
  padding: 15px;
  flex-wrap: nowrap;
  .van-row {
    flex-wrap: nowrap;
  }
  .van-col {
    flex-shrink: 0;
  }
  .user {
    flex: 1 1 auto;
    min-width: 0;
  }
  .head {
    overflow: hidden;
    border-radius: 50%;
    width: 50px;height: 50px;
    margin-right: 15px;
    img {
      display: block;
      width: 100%;
    }
  }
  .sub {font-size: 12px;color: #888;}
  .info {
    color: #888;
    margin-top: 5px;font-size: 12px;
  }
}
/deep/ .lang .van-stepper__input {
  width: calc(100% - 60px);
}
.tip {
  padding: 5px 15px;
  font-size: 12px;
  color: #888;
  background: #fff;
}
.title {
  padding: 10px 15px;
}
.tip2 {
  padding: 15px;
  font-size: 12px;
  color: #888;
  h3 {
    margin-bottom: 5px;
    font-weight: normal;
  }
}
.ft-btn {
  padding: 15px;
}
</style>
