<template>
  <div>
    <van-nav-bar
      :title="$t('title')"
      left-arrow
      :right-text="$t('buy')"
      @click-left="$router.back()"
      @click-right="showPwd = true"
    />
    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list v-model="loading" :finished="finished" :finished-text="$t('finished_text')" @load="onLoad">
        <div v-for="item in list" :key="item.id" class="key-item">
          <van-row type="flex" justify="space-between" align="center">
            <van-col class="title">{{ $t('key') }}：{{ item.keys }}</van-col>
            <van-col v-if="!item.used">
              <copy
                v-clipboard:copy="item.keys"
                v-clipboard:success="onCopy"
                theme="outline"
                size="16"
                fill="#323233"
                :stroke-width="2"
              />
            </van-col>
          </van-row>
          <van-row type="flex" justify="space-between" align="center">
            <van-col class="time">{{ $t('time') }}：{{ item.ctime | timeFormat }}</van-col>
            <van-col>
              <span v-if="item.used" class="status">{{ $t('state') }}({{ $t('robot') }} ID:{{ item.qrobot_id }})</span>
            </van-col>
          </van-row>
        </div>
      </van-list>
    </van-pull-refresh>
    <!-- <password-confirm :show="showPwd" @close="showPwd = false" @confrim="buyCdkey" /> -->
    <van-dialog v-model="showPwd" :title="$t('msg.Purchase_activation_code')/*购买激活码*/" show-cancel-button @confirm="buyCdkey">
      <div class="dialog-1">
        <van-cell>
          <span class="label">{{ $t('msg.Purchase_quantity') }}<!-- 购买数量 --></span>
          <span>1</span>
        </van-cell>
        <van-cell>
          <span class="label">{{ $t('msg.transaction_password') }}<!-- 交易密码 --></span>
          <input v-model="pwd" type="password" :placeholder="$t('msg.Please_enter_transaction_password')/*请输入交易密码*/">
        </van-cell>
        <div class="tip">{{ $t('msg.To_pay') }}<!-- 支付： --><span>{{ initInfo.cdkey_price }}</span> USDT</div>
      </div>
    </van-dialog>
  </div>
</template>

<script>
import { Copy } from '@icon-park/vue'
import { mapState, mapActions } from 'vuex'
import PasswordConfirm from '@/components/common/PasswordConfirm'
export default {
  components: { Copy, PasswordConfirm },
  i18n: {
    messages: {
      zh: {
        title: '激活码',
        buy: '购买激活码',
        key: '激活码',
        time: '获得时间',
        state: '已使用',
        robot: '机器人'
      },
      en: { title: 'CD-Key', buy: 'Buy', key: 'CD-Key', time: 'Get Time', state: 'Used', robot: 'Robot' },
      hk: {
        title: '激活碼',
        buy: '購買激活碼',
        key: '激活碼',
        time: '獲得時間',
        state: '已使用',
        robot: '機械人'
      }
    }
  },
  data () {
    return {
      show: true,
      showPwd: false,
      loading: false,
      finished: false,
      refreshing: false,
      list: [],
      pwd: ''
    }
  },
  computed: {
    ...mapState({
      initInfo: index => index.initInfo
    })
  },
  methods: {
    ...mapActions({
      cdkeyList: 'user/cdkeyList',
      cdkeyActive: 'user/cdkeyActive',
      cdkeyBuy: 'user/cdkeyBuy'
    }),
    onLoad () {
      this.cdkeyList()
        .then((res) => {
          this.list = res.data
        })
        .finally(() => {
          this.loading = false
          this.finished = true
        })
    },
    onRefresh () {
      this.finished = false
      this.loading = true
      this.onLoad()
    },
    onCopy () {
      this.$toast(this.$t('msg.Copy_successfully'))/* '复制成功' */
    },
    buyCdkey (password) {
      this.showPwd = false
      this.$toast.loading()
      password = password || this.pwd
      this.cdkeyBuy({ password })
        .then((res) => {
          this.$toast(res.msg)
          this.onRefresh()
        })
        .catch(({ msg }) => {
          this.$toast(msg)
        })
    }
  }
}
</script>

<style scoped lang="less">
.key-item {
  margin: 10px 15px;
  padding: 10px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 5px 5px 15px -5px rgba(0, 0, 0, 0.05);
  line-height: 30px;
}
.title {
  font-weight: 500;
}
.time {
  color: #999999;
  font-size: 12px;
}
.status {
  font-size: 12px;
  color: red;
  opacity: 0.6;
}
.btn {
  display: block;
  height: auto;
  padding: 5px 10px;
}
.dialog-1 {
  padding: 20px 10px;
  .van-cell__value {
    display: flex;align-items: center;
  }
  .label {
    width: 5em;
    flex-shrink: 0;
  }
  input {
    border: none;
    flex-grow: 1;
    min-width: 0;
  }
  .tip {
    text-align: right;
    padding: 10px 16px;
    font-size: 12px;
    span {
      color: blue;
    }
  }
}
</style>
