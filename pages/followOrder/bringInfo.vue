<template>
  <div class="page">
    <van-nav-bar
      title="DJ黑天鹅"
      left-arrow
      @click-left="$router.back()"
    />
    <div class="item-hd">
      <div class="user">
        <van-row type="flex" align="center">
          <van-col><div class="head"><img src="@/assets/images/header.png"/></div></van-col>
          <van-col class="user">
            <div style="font-size: 1.2em">DJ黑天鹅</div>
            <van-row class="info">
              <van-col>
                <div class="label">已入驻</div>
                <div class="value">86天</div>
              </van-col>
              <van-col>
                <div class="label">盈利分成</div>
                <div class="value">+10%</div>
              </van-col>
            </van-row>
          </van-col>
        </van-row>
        <div class="desc">简单重复简单重复简单重复简单重复简单重复简单重复</div>
      </div>
    </div>
    <div class="tab-nav van-hairline--bottom">
      <div :class="['item', active === 1 ? 'active' : '']" @click="active = 1">带单概况</div>
      <div :class="['item', active === 2 ? 'active' : '']" @click="active = 2">历史带单</div>
    </div>
    <van-row v-if="active === 1" class="bring-row">
      <van-col>
        <div class="label van-ellipsis">累计收益率</div>
        <div class="van-ellipsis">+400.82%</div>
      </van-col>
      <van-col>
        <div class="label van-ellipsis">近2周交易胜率</div>
        <div class="van-ellipsis">+87.82%</div>
      </van-col>
      <van-col>
        <div class="label van-ellipsis">总收益(USDT)</div>
        <div class="van-ellipsis">16481.29</div>
      </van-col>
      <van-col>
        <div class="label van-ellipsis">交易胜率</div>
        <div class="van-ellipsis">+0.72%</div>
      </van-col>
      <van-col>
        <div class="label van-ellipsis">交易笔数</div>
        <div class="van-ellipsis">510</div>
      </van-col>
      <van-col>
        <div class="label van-ellipsis">跟单人数</div>
        <div class="van-ellipsis">461人</div>
      </van-col>
      <van-col>
        <div class="label van-ellipsis">交易频次</div>
        <div class="van-ellipsis">52次/周</div>
      </van-col>
    </van-row>
    <van-list v-if="active === 2">
      <div class="order-item van-hairline--bottom">
        <div class="hd">
          <van-tag color="rgba(19,184,135,.15)" text-color="#13b887">做多</van-tag>
          ETH/USDT 逐仓 5X
        </div>
        <div class="info">
          <van-row class="bring-row">
            <van-col>
              <div class="label van-ellipsis">开仓均价</div>
              <div class="van-ellipsis">1300.0000</div>
            </van-col>
            <van-col>
              <div class="label van-ellipsis">平仓均价</div>
              <div class="van-ellipsis">1345.9000</div>
            </van-col>
            <van-col>
              <div class="label van-ellipsis">收益率</div>
              <div class="van-ellipsis">+17.65%</div>
            </van-col>
            <van-col>
              <div class="label van-ellipsis">开仓时间</div>
              <div class="van-ellipsis">2021-02-28 <br>23:44:36</div>
            </van-col>
            <van-col>
              <div class="label van-ellipsis">平仓时间</div>
              <div class="van-ellipsis">2021-02-28 <br>23:44:36</div>
            </van-col>
          </van-row>
        </div>
      </div>
      <div class="order-item van-hairline--bottom">
        <div class="hd">
          <van-tag color="rgba(235,77,92,.15)" text-color="#eb4d5c">做空</van-tag>
          ETH/USDT 逐仓 5X
        </div>
        <div class="info">
          <van-row class="bring-row">
            <van-col>
              <div class="label van-ellipsis">开仓均价</div>
              <div class="van-ellipsis">1300.0000</div>
            </van-col>
            <van-col>
              <div class="label van-ellipsis">平仓均价</div>
              <div class="van-ellipsis">1345.9000</div>
            </van-col>
            <van-col>
              <div class="label van-ellipsis">收益率</div>
              <div class="van-ellipsis">+17.65%</div>
            </van-col>
            <van-col>
              <div class="label van-ellipsis">开仓时间</div>
              <div class="van-ellipsis">2021-02-28 <br>23:44:36</div>
            </van-col>
            <van-col>
              <div class="label van-ellipsis">平仓时间</div>
              <div class="van-ellipsis">2021-02-28 <br>23:44:36</div>
            </van-col>
          </van-row>
        </div>
      </div>
    </van-list>
    <div class="ft-btn">
      <van-button block type="primary" @click="$router.push('/followOrder/form')">立即跟单</van-button>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      active: 1
    }
  }
}
</script>

<style lang="less" scoped>
.item-hd {
  background-color: #fff;
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
    width: 60px;height: 60px;
    margin-right: 15px;
    img {
      display: block;
      width: 100%;
    }
  }
  .sub {font-size: 12px;color: #888;}
  .desc {
    color: #888;
    margin-top: 10px;font-size: 12px;
  }
  .info {
    font-size: 12px;
    .van-col {
      margin-right: 15px;
    }
    .label {
      transform-origin: 0 50%;
      transform: scale(.8);
      color: #888;
      margin-bottom: 5px;
    }
  }
}
.page {
  min-height: 100vh;
  background-color: #fff;
  padding-bottom: 72px;
}
.ft-btn {
  position: fixed;
  bottom: 0;left: 0;width: 100%;
  padding: 15px;
  background-color: #fff;
}
.tab-nav {
  display: flex;align-items: center;
  .item {
    position: relative;
    font-size: 1.3em;
    font-weight: 500;
    padding: 0 15px;
    line-height: 3;
    opacity: .6;
    &.active {
      opacity: 1;
      &::after {
        content: '';
        position: absolute;
        bottom: 0;left: 50%;margin-left: -7.5px;
        border-radius: 5px;
        width: 15px;height: 3px;
        background-color: rgb(48, 120, 255);
      }
    }
  }
}
.bring-row {
  padding: 15px;
  font-size: 14px;
  display: flex;flex-wrap: wrap;
  .van-col {
    flex: 0 1 auto;
    width: 40%;
    padding: 0 5px;
    margin-bottom: 15px;
    &:nth-child(3n-1) {
      width: 30%;
    }
    &:nth-child(3n) {
      width: 30%;
      text-align: right;
    }
  }
  .label {
    font-size: 0.8em;
    color: #888;
    margin-bottom: 5px;
  }
}
.order-item {
  .hd {
    display: flex;align-items: center;
    height: 40px;
    padding: 0 15px;
    font-size: 1.2em;
    .van-tag {margin-right: 10px;}
  }
  .bring-row {
    padding: 10px 15px 5px;
  }
}
</style>
