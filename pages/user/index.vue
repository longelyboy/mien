<template>
  <div>
    <div class="top-cover">
      <div safe-area-inset-top>
        <van-row
          type="flex"
          justify="space-between"
          align="center"
          class="page-header"
        >
          <van-col class="page-header-left">
            <h2 class="page-title">{{ $t('nav.user') }}</h2>
          </van-col>
          <van-col
            v-if="logged"
            class="page-header-right"
          >
            <nuxt-link to="/user/settings">
              <van-icon
                name="setting-o"
                color="#999"
                size="20"
              />
            </nuxt-link>
          </van-col>
        </van-row>
      </div>
      <van-row
        v-if="logged"
        type="flex"
        justify="space-between"
        align="center"
        gutter="20"
        class="user-info"
      >
        <van-col style="flex: 1; min-width: 0">
          <van-row
            type="flex"
            align="center"
          >
            <van-col>
              <van-image
                class="avatar"
                width="60"
                :src="userInfo.avatar"
              ></van-image>
            </van-col>
            <van-col style="flex: 1; min-width: 0">
              <div class="user-nickname">{{ userInfo.user_nickname }}</div>

              <div class="user-level">{{ userInfo.level_name }}</div>

              <!-- <div class="user-account">{{ userInfo.signature }}</div> -->
              
              <div v-if="BUY_PACKAGE" class="user-tip">
                <template v-if="userInfo.vip_deadline > 0">
                  {{ `${$t('tip1')}：${ format(userInfo.vip_deadline, '{y}-{m}-{d}') }` }}
                </template>
                <template v-else>
                  {{ $t('tip2') }}
                </template>
              </div>
            </van-col>
          </van-row>
        </van-col>
        <van-col>
          <div
            v-if="hasCDKey"
            class="user-links"
            @click="$refs.cdkey.showCodePop = true"
          >
            <van-icon name="coupon-o" />
            {{ $t('cdkey') }}
          </div>
        </van-col>
      </van-row>
      <van-row
        v-else
        class="user-info"
        type="flex"
        align="center"
        @click="$router.push('/sign/login')"
      >
        <van-col>
          <van-icon
            class="avatar"
            name="user-circle-o"
            size="60"
          />
        </van-col>
        <van-col>
          <div class="user-nickname">{{ $t('pageUser.login') }}</div>
          <div class="user-account">{{ $t('pageUser.welcome') }}</div>
        </van-col>
      </van-row>
    </div>

    <van-cell-group class="list-group">
      <van-cell
        icon="balance-o"
        :title="$t('pageUser.asset')"
        is-link
        @click="handleLink('/wallet?symbol=USDT')"
      />
      <!-- <van-cell
        v-if="initInfo.quant_revenue_type==2"
        icon="fire-o"
        :title="`${initInfo.system_balance_name}${$t('pageUser.ranliao')}`"
        is-link
        @click="handleLink('/wallet/index2')"
      /> -->
      <van-cell
        icon="records"
        :title="$t('pageUser.history')"
        is-link
        @click="handleLink('/user/caleandar')"
      />
      <van-cell
        v-if="hasCDKey"
        icon="points"
        :title="$t('pageUser.cdkey')"
        is-link
        @click="handleLink('/user/activation')"
      />
      <van-cell
        v-if="BUY_PACKAGE"
        icon="cart-o"
        :title="$t('buyPackage')"
        is-link
        @click="handleLink('/buyPackage')"
      />
    </van-cell-group>

    <van-cell-group
      v-if="0"
      class="list-group"
    >
      <van-cell
        icon="manager"
        :title="$t('pageUser.safety_lv')"
        is-link
        @click="handleLink('/user/verified')"
      />
      <van-cell
        icon="youzan-shield"
        :title="$t('pageUser.google_valid')"
        is-link
        @click="handleLink('/user/googleValid')"
      />
    </van-cell-group>

    <van-cell-group>
      <van-cell
        icon="user-o"
        :title="$t('pageUser.community')"
        is-link
        @click="handleLink('/user/invite')"
      />
      <van-cell
        icon="qr"
        :title="$t('pageUser.invite')"
        is-link
        @click="handleLink('/user/invite/poster')"
      />
      <van-cell
        icon="orders-o"
        :title="$t('pageUser.about')"
        is-link
        @click="goAbout()"
      />
      <van-cell
        icon="chat-o"
        :title="$t('contact')"
        is-link
        @click="goHelp()"
      />
    </van-cell-group>
    <activation-popup ref="cdkey" />
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import ActivationPopup from './activation/ActivationPopup'
import { format } from '@/utils/time'
import { BUY_PACKAGE, CHEKC_CDKEY } from '@/config/index'

export default {
  layout: 'navigation',
  i18n: {
    messages: {
      zh: {
        contact: '联系我们',
        language: '选择语言',
        tip1: '您的vip身份到期时间为',
        tip2: '您的vip身份已到期！'
      },
      en: {
        contact: 'Contact Us',
        language: 'Change Language',
        tip1: 'Your VIP status expires at',
        tip2: 'Your vip status has expired!'
      }
    }
  },
  components: {
    ActivationPopup
  },
  data () {
    return {
      BUY_PACKAGE,
      hasCDKey: CHEKC_CDKEY,
      activationCode: ''

    }
  },
  computed: {
    ...mapState({
      logged: ({ user }) => user.logged,
      userInfo: ({ user }) => user.userInfo,
      initInfo: index => index.initInfo,
      thirdLoginEnabled: ({ thirdLoginEnabled }) => thirdLoginEnabled
    }),
    ...mapActions({
      getUserInfo: 'user/getUserInfo'
    })
  },
  methods: {
    async getUserInfo1() {
      await this.getUserInfo
    },
    startCallBack () {
      this.$refs.LuckyWheel.play()
      setTimeout(() => {
        this.$refs.LuckyWheel.stop(Math.random() * 8 >> 0)
      }, 1000)
    },
    format,
    handleLink (path) {
      if (this.logged) {
        this.$router.push(path)
      } else {
        this.$router.push('/sign/login')
      }
    },
    goAbout() {
      this.$router.push({
        name: 'common-article',
        params: {
          url: this.initInfo.system_user_agreement,
          title: '服务协议'
        }
      })
    },
    game() {
      this.$router.push('/user/game')
    },
    goHelp() {
      this.$router.push({
        name: 'common-article',
        params: {
          url: this.initInfo.system_customer_service,
          title: '联系我们'
        }
      })
    }
  },
  created() {
    this.getUserInfo1()
  }
}
</script>

<style scoped lang="less">
.top-cover {
  background-color: #fff;
}
.page-header {
  height: 46px;
  padding: 0 15px;
  margin-bottom: 20px;
  &-right .van-icon {
    display: inline-block;
    vertical-align: middle;
  }
  &-title {
    display: flex;
    align-items: center;
    font-size: 22px;
    line-height: 1;
    color: #333333;
  }
}
.van-cell-group {
  margin-top: 10px;
}
.user-info {
  padding: 15px;
  font-size: 14px;
  line-height: 1;
  .avatar {
    display: block;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    margin-right: 15px;
    overflow: hidden;
  }
}
.user-nickname {
  font-size: 18px;
  font-weight: 500;
}
.user-account {
  margin-top: 6px;
}
.user-level{
  width: 70px;
  text-align: center;
  height: 20px;
  line-height: 20px;
  border-radius: 3px;
  margin-top: 6px;
  font-size: 0.26rem;
  color: rgb(255, 255, 255);
  background: rgb(24, 69, 141);
  padding: 0px 0.15rem;
  
}
.user-tip {
  font-size: 12px;
  margin-top: 5px
}
.user-links {
  text-align: center;
  font-size: 12px;
  .van-icon {
    font-size: 18px;
    display: block;
    margin-bottom: 5px;
  }
}
/deep/ .van-dialog__content {
  padding: 30px 15px;
  .van-cell-group {
    margin-top: 0;
  }
}
</style>
