<template>
  <div>
    <van-nav-bar
      :title="$t('followTitle')"
      left-arrow
      @click-left="$router.back()"
    />
    <div class="tab">
      <div class="tab-hd">
        <div class="van-hairline--bottom">
          <van-row type="flex" justify="space-between" align="center">
            <van-col class="title">交易员列表</van-col>
            <van-col><nuxt-link to="/followOrder/myCopyTrading">我的跟单</nuxt-link></van-col>
          </van-row>
        </div>
        <van-row type="flex" justify="space-between" align="center">
          <van-col>USDT带单</van-col>
          <van-col>
            <van-button size="mini" :class="[active === 1 ? 'active' : '']" @click="onChange(1)">收益额</van-button>
            <van-button size="mini" :class="[active === 2 ? 'active' : '']" @click="onChange(2)">收益率</van-button>
            <van-button size="mini" :class="[active === 3 ? 'active' : '']" @click="onChange(3)">胜率</van-button>
          </van-col>
        </van-row>
      </div>
      <div class="tab-bd">
        <van-list>
          <div class="item" @click="$router.push('/followOrder/bringInfo')">
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
              <van-col class="btn"><van-button type="primary" size="small" style="padding: 0 20px" @click.stop="$router.push('/followOrder/form')">跟单</van-button></van-col>
            </van-row>
            <div class="item-info">
              <van-row >
                <van-col span="8">
                  <div class="label van-ellipsis">累计收益率</div>
                  <div class="van-ellipsis">+400.82%</div>
                </van-col>
                <van-col span="8">
                  <div class="label van-ellipsis">近2周交易胜率</div>
                  <div class="van-ellipsis">+87.82%</div>
                </van-col>
                <van-col span="8">
                  <div class="label van-ellipsis">总收益(USDT)</div>
                  <div class="van-ellipsis">16481.29</div>
                </van-col>
                <van-col span="8">
                  <div class="label van-ellipsis">额度限制</div>
                  <div class="van-ellipsis">100.00 - 1000.00</div>
                </van-col>
                <van-col span="8">
                  <div class="label van-ellipsis">上次交易时间</div>
                  <div class="van-ellipsis">58分钟前</div>
                </van-col>
              </van-row>
            </div>
          </div>
        </van-list>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      active: 1
    }
  },
  mounted() {
    console.log(this)
  },
  methods: {
    onChange (index) {
      this.active = index
    }
  }
}
</script>

<style scoped lang="less">
.tab-hd {
  background-color: #fff;
  .van-row {
    padding: 8px 15px;
  }
  .van-button {
    padding: 0 10px;
    border-radius: 4px;
    &.active {
      --color: rgb(48, 120, 255);
      border-color: var(--color);
      color: var(--color);
    }
  }
}
.title {
  font-size: 1.2em;
}
.item {
  display: block;
  margin: 10px 0;
  background-color: #fff;
}
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
.item-info {
  font-size: 12px;
  .van-col {
    padding: 0 15px;
    margin-bottom: 15px;
  }
  .label {
    transform-origin: 0 50%;
    transform: scale(.8);
    color: #888;
    margin-bottom: 5px;
  }
}
</style>
