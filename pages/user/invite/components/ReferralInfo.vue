<template>
  <div>
    <div v-if="info" class="user-info">
      <div class="tag">
        {{ $t('msg.Your_level') }}<!-- 您的等级： -->{{ info.my_info.is_partner === 1 ? $t('msg.partner')/*'合伙人'*/ : $t('msg.user')/*'用户'*/ }} <van-tag round color="#7232dd">Lv.{{ info.my_info.level_id }}</van-tag>
      </div>
      <van-row class="info" type="flex" justify="space-between">
        <van-col :span="8"><p class="label">{{ $t('msg.Agent_status') }}<!-- 代理身份 --></p><p class="value">{{ info.my_info.level_name }}</p></van-col>
        <van-col :span="8"><p class="label">{{ $t('msg.Dividend_ratio') }}<!-- 分红比例 -->(%)</p><p class="value">{{ info.my_info.profit_rate }}</p></van-col>
        <van-col :span="8"><p class="label">{{ $t('msg.Total_promotion_performance') }}<!-- 总推广业绩 --></p><p class="value">{{ info.my_info.total }}</p></van-col>
      </van-row>
    </div>
    <div class="referral-info">
      <div class="total">
        <div class="lab">{{ $t('total') }}</div>
        <div class="val">{{ Number(info.total_all_sum).toFixed(5) || 0 }} USDT</div>
      </div>
      <div class="reg">{{ $t('invite') }} {{ info.total_reg_count }} 人</div>
      <div class="items">
        <div class="item">
          <div class="val">{{ info.count_reg_1 }}</div>
          <div class="lab">{{ $t('number_1') }}</div>
        </div>
        <div class="item">
          <div class="val">{{ info.count_reg_2 }}</div>
          <div class="lab">{{ $t('number_2') }}</div>
        </div>
        <div class="item">
          <div class="val">{{ info.count_reg_3 }}</div>
          <div class="lab">{{ $t('number_3') }}</div>
        </div>
      </div>
      <!-- <div class="reg">{{ $t('active') }} {{ info.total_deposit_count }} 人</div>
      <div class="items">
        <div class="item">
          <div class="val">{{ info.invite_1_deposit_parent_reward }}</div>
          <div class="lab">{{ $t('number_1') }}</div>
        </div>
        <div class="item">
          <div class="val">{{ info.invite_2_deposit_parent_reward }}</div>
          <div class="lab">{{ $t('number_2') }}</div>
        </div>
        <div class="item">
          <div class="val">{{ info.invite_3_deposit_parent_reward }}</div>
          <div class="lab">{{ $t('number_3') }}</div>
        </div>
      </div> -->
    </div>
  </div>
</template>
<script>
import { Tag } from 'vant'
import { mapActions } from 'vuex'
export default {
  i18n: {
    messages: {
      zh: {
        total: '累计邀请分润奖励',
        invite: '好友邀请人数',
        active: '好友激活人数',
        number: '好友注册人数',
        number_1: '直属好友数',
        number_2: '隶属好友数',
        number_3: '其余好友数'
      },
      en: {
        total: 'Cumulative Invitation Registration Bonus',
        invite: 'Number of friends inviting',
        active: 'Number of friends activating',
        number: 'Number of friends registered',
        number_1: 'Number of first-level friends',
        number_2: 'Number of secondary friends',
        number_3: 'Number of third-level friends'
      },
      hk: {
        total: '累計邀請分潤獎勵',
        invite: '好友邀請人數',
        active: '好友激活人數',
        number: '好友註冊人數',
        number_1: '直屬好友數',
        number_2: '隸屬好友數',
        number_3: '其餘好友數'
      }
    }
  },
  components: {
    [Tag.name]: Tag
  },
  data () {
    return {
      info: ''
    }
  },
  beforeMount () {
    this.invitationInfo()
      .then((data) => {
        this.info = data.data
      })
  },
  methods: {
    ...mapActions({
      invitationInfo: 'user/invitationInfo'
    })
  }
}
</script>
<style scoped lang="less">
.referral-info {
  margin: 15px;
  padding: 0 10px;
  border-radius: 10px;
  background: rgb(66, 65, 65);
  text-align: center;
  line-height: 25px;
}
.referral-info .total {
  padding: 20px 20px 10px;
}
.referral-info .total .lab {
  color: #fff;
  font-size: 16px;
}
.referral-info .total .val {
  color: rgb(208, 209, 128);
  font-size: 16px;
}
.referral-info .total .val {
  font-weight: bold;
}
.referral-info .items {
  border-top: 1px solid rgba(255, 255, 255, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px 0;
}
.referral-info .item {
  flex: 1 0 0;
}
.referral-info .item .val {
  font-size: 15px;
  font-weight: bold;
  color: #fff;
}
.referral-info .item .lab {
  font-size: 14px;
  color: #fff;
  margin-top: 5px;
}
.reg {
  color: #fff;
  padding-bottom: 15px;
  font-size: 16px;
}
.user-info {
  background-color: #fff;
  padding: 10px 15px;
  .tag {
    font-size: 16px;
    margin-bottom: 10px;
  }
  .van-col ~ .van-col {
    position: relative;
    &::before {
      content: '';
      position: absolute;
      top: 15%;bottom: 15%;left: 0;
      width: 1px;background-color: #eee;
      transform: scaleX(.5);
    }
  }
  .info {
    padding: 10px 0;
    text-align: center;
  }
  .label {
    margin-bottom: 10px;
    font-size: 12px;
    color: #888;
  }
  .value {
    font-size: 16px;
  }
}
</style>
