<template>
  <div>
    <van-nav-bar
      :border="false"
      :title="$t('pageRobot.robot_setup')"
      left-arrow
      @click-left="$router.back()"
    />
    <van-form label-width="32%">
      <van-field
        :value="market"
        readonly
        clickable
        :label="$t('pageRobot.trade_area')"
        :placeholder="$t('pageRobot.trade_area')"
        :rules="[{ required: true }]"
        style="background:#F5F6F7;color:#333;font-weight: 700;"
        @click="onMarket"
      />
      <h3 class="title">预设策略</h3>
      <van-row class="preset">
        
        <van-col>
          <van-button
            block
            size="small"
            :type="preset === 3 ? 'primary' : 'default'"
            @click="changePreset(3)"
          >
            稳健
          </van-button>
        </van-col>
        <van-col>
          <van-button
            block
            size="small"
            :type="preset === 4 ? 'primary' : 'default'"
            @click="changePreset(4)"
          >
            自定义
          </van-button>
        </van-col>
      </van-row>
      <van-field
        v-model="first_order_value"
        :label="$t('first_order_num')"
        :placeholder="$t('first_order_num')"
        :rules="[{ required: true}]"
      />
       <van-field
        :label="$t('first_order_num1')"
      >
      <template #input>
        {{firstOrderValueU}}
      </template>
      </van-field>
      <van-field
        v-model="price"
        :label="$t('first_order_price')"
        :placeholder="$t('first_order_price')"
        :rules="[{ required: true }]"
      />

      <van-field label="">
        <template #input>
          最低买价：{{robotPrice.low_limit}} &nbsp; 最高买价：{{robotPrice.high_limit}}
        </template>
      </van-field>

      <van-field name="radio" label="">
        <template #input>
          <van-radio-group v-model="checked" direction="horizontal">
            <van-radio :name="1">等额</van-radio>
            <van-radio :name="2">倍额</van-radio>
            <van-radio :name="3">
              差额
            </van-radio>
          </van-radio-group>
        </template>
      </van-field>

      

      <van-field
        v-model="max_order_count"
        type="digit"
        :label="$t('number_of_orders')"
        :placeholder="$t('number_of_orders')"
        :rules="[{ required: true }]"
      />

      
      <van-field
        v-model="stop_profit_rate"
        :label="$t('take_profit_ratio') + '(%)'"
        :placeholder="$t('take_profit_ratio')"
        :rules="[{ required: true }]"
      />
      <van-field
        v-model="stop_profit_callback_rate"
        :label="$t('take_profit_retracement') + '(%)'"
        :placeholder="$t('take_profit_retracement')"
        :rules="[{ required: true }]"
      />
      <!-- <van-field v-model="cover_rate" :label="$t('cover_down') + '(%)'" :placeholder="$t('cover_down')" :rules="[{ required: true }]"
      /> -->
      <van-field readonly :label="$t('cover_down') + '(%)'" :rules="[{ required: true }]">
        <van-button
          slot="button"
          size="small"
          type="primary"
          class="setting"
          @click="showSetting()"
        >
          {{ $t('setting') }}
        </van-button>
      </van-field>
      <van-field
        v-model="cover_callback_rate"
        :label="$t('cover_pullback') + '(%)'"
        :placeholder="$t('cover_pullback')"
        :rules="[{ required: true }]"
      />

      <van-field
        v-model="sl_trigger_price"
        :label="$t('sl_trigger_price') + '(%)'"
        :placeholder="$t('sl_trigger_price')"
        :rules="[{ required: true }]"
      />
      
      <van-field name="radio" :label="$t('direction')">
        <template #input>
          <van-radio-group v-model="direction" direction="horizontal">
            <van-radio :name="1">{{ $t('directionbuy') }}</van-radio>
            <van-radio :name="2">{{ $t('directionsell') }}</van-radio>
          </van-radio-group>
        </template>
      </van-field>
      <van-field
        v-if="formType === 'create' && CHEKC_CDKEY"
        v-model="cd_key"
        :label="$t('cdkey')"
        :placeholder="$t('cdkey')"
        :rules="[{ required: true }]"
      />
      <div v-if="formType === 'create'" class="tips">
        {{ $t('tip') }}：{{ initInfo.quant_startup_min }} {{ initInfo.quant_revenue_type === '2' ? initInfo.system_balance_name : 'USDT' }}
      </div>
      <div style="padding: 16px;">
        <van-button round block type="info" @click="onSubmit">
          {{ $t('actions.submit') }}
        </van-button>
      </div>
    </van-form>
    <van-popup v-model="marketPicker" position="bottom">
      <van-picker
        show-toolbar
        :columns="marketLists"
        value-key="market_name"
        @confirm="onConfirm"
        @cancel="marketPicker = false"
      />
    </van-popup>
    <van-popup v-model="show" position="bottom" class="list_box">
      <!-- <div v-show="show" class="box_"> -->
      <div>
        <p>{{ $t('cover_down') }} <span style="float:right;color:#999;" @click="show = false">    {{ $t('actions.cancel') }}</span></p>
        <ul classs="listInput">
          <li v-for="(item,index) in listInput" :key="index" class="list" style="overflow: hidden;text-align: right;border: none;padding:10px;border-bottom: 1px solid #ebedf0;">
            <span v-if="index===0" style=" float: left;" class="list_span">{{ $t('Cover') }}</span>
            <span v-else style=" float: left;" class="list_span">第{{ item.count }}次补仓</span>
            <i style=" float: right;" class="list_i">%</i>
            <input v-model="item.input" class="list_input" min="0.01" max="50" type="number" style=" float: right;border:none;margin-right:10px;text-align:right;" @input="handleInput(e,item)" >
            <!-- @input="inputMaxL = /^\d+\.?\d{0,1}$/.test(item.input) ? null : item.input.length - 1" -->
          <!--  -->
          <!--  -->
          </li>
        </ul>
        <div class="van-button--info" @click="buttoninfo">确定</div>
      </div>
    <!-- </div> -->
    </van-popup>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import { CHEKC_CDKEY } from '@/config/index'
import API from '@/constants/api'
export default {
  i18n: {
    messages: {
      zh: {
        tip: '启动机器人最小余额'
      },
      en: {
        tip: 'Start robot minimum balance'
      }
    }
  },
  data() {
    return {
      checked: 2,
      CHEKC_CDKEY,
      preset: 4,
      formType: 'create',
      marketPicker: false,
      market: '',
      money: '',
      platform: 'huobi',
      robot_id: '',
      market_id: '',
      first_order_value: '100',
      max_order_count: '',
      stop_profit_rate: '',
      number:0,
      stop_profit_callback_rate: '',
      cover_rate: '',
      cover_callback_rate: '',
      direction: 1,
      price: '',
      sl_trigger_price: '',
      cd_key: '',
      recycle_status:0,
      show: false,
      listInput: [],
      robotPrice:{},
      contract_size:0,
      defaultStrategy:{},
      customStrateg:{}
    }
  },
  computed: {
    ...mapState({
      initInfo: index => index.initInfo,
      robotList: ({ robot }) => robot.robotList,
      thirdLoginEnabled: ({ thirdLoginEnabled }) => thirdLoginEnabled
    }),
    ...mapGetters({
      markets: 'robot/markets'
    }),
    marketLists() {
      return this.markets(this.platform) || []
    },
    firstOrderValueU(){
      //张数 * 面值 * 价格 /  20  （marketList）
      const first_order_value = +this.first_order_value;
      const price = +this.price || 1;
      const contractSize = +this.contract_size;
      return (first_order_value * contractSize * price / 5).toFixed(6);
    }
  },

  async created() {
    if(this.$route.query.data){
      this.queryData = JSON.parse(this.$route.query.data);
    }
    
    this.formType = this.$route.query.type
    if (this.formType === 'edit') {
      const robot = (this.robot = this.robotList.find(
        item => this.$route.query.robot_id === item.id
      ))
      this.queryData = robot;
      // this.listInput [ {count: 1,input: ""} ]
      console.log(robot)
      this.$nextTick(() => {
        
        this.platform = robot.platform
        this.checked = robot.c_type
        this.market = robot.market_name
        this.market_id = robot.market_id
        this.robot_id = robot.id
        this.first_order_value = robot.first_order_value
        this.max_order_count = robot.max_order_count
        this.stop_profit_rate = robot.stop_profit_rate
        this.number = robot.number
        this.stop_profit_callback_rate = robot.stop_profit_callback_rate
        this.cover_rate = robot.cover_rate
        this.cover_callback_rate = robot.cover_callback_rate
        this.direction = robot.direction
        this.money = robot.money
        this.price = robot.price
        this.sl_trigger_price = robot.sl_trigger_price
        this.listInput = []
      })
    } else {
      
      const markets = this.queryData
      this.platform = this.$route.query.platform
      this.market = markets.market_name
      this.market_id = markets.id
      this.money = markets.money
    }

    this.marketList({
        platform: this.platform,
        type: 'swap'
      })
      await this.getStrategy();
    await this.getLimitPrice()
     const timer = setInterval(async () => {
        await this.getLimitPrice()
      }, 5000);
     this.$once('hook:beforeDestroy', () => {
      clearTimeout(timer)
    })
    await this.getContractSize()
   
  },
  methods: {
    showSetting() {
      this.listInput = []
      if (this.cover_rate == '') {
        if (this.max_order_count > 0) {
          for (let i = 0; i < this.max_order_count; i++) {
            const obj = {}
            obj.count = ''
            obj.input = ''
            this.listInput.push(obj)
          }
          this.listInput.map((item, index) => {
            item.count = index + 1
          })
        }
      } else {
        this.listInput = []
        const obj = JSON.parse(this.cover_rate)
        const arr = []
        for (const key in obj) {
          const obj1 = {}
          obj1.count = ''
          obj1.input = obj[key]
          arr.push(obj1)
        }
        this.listInput = arr
        this.listInput.map((item, index) => {
          item.count = index + 1
        })

        const obj2 = JSON.parse(this.cover_rate)
        const arr2 = []
        for (const key in obj2) {
          const obj1 = {}
          obj1.count = ''
          obj1.input = obj[key]
          arr2.push(obj1)
        }

        if (arr2.length != this.max_order_count) {
          for (let i = 0; i < this.max_order_count - arr2.length; i++) {
            const obj = {}
            obj.count = ''
            obj.input = ''
            this.listInput.push(obj)
          }
        }
        this.listInput.map((item, index) => {
          item.count = index + 1
        })
      }

      // if (this.max_order_count > 0) {
      //   for (let i = 0; i < this.max_order_count; i++) {
      //     const obj = {}
      //     obj.count = ''
      //     obj.input = ''
      //     this.listInput.push(obj)
      //   }
      // }

      // for (let i = 0; i < this.listInput; i++) {
      //   console.log(this.listInput[i])
      //   this.listInput[i].count = i + 1
      // }

      console.log(this.listInput)
      this.show = true

      // for (let i = 0; i < this.cover_rate; i++) {
      //   console.log(this.listInput)
      // }
      // } else {
      //   const obj = JSON.parse(this.cover_rate)
      //   const arr = []
      //   let num = 0
      //   for (const key in obj) {
      //     const obj1 = {}
      //     obj1.count = num += 1
      //     obj1.input = obj[key]
      //     arr.push(obj1)
      //   }
      //   this.listInput = arr
      //   console.log(this.listInput)
      //   this.show = true
      // }
    },
    buttoninfo() {
      this.cover_rate = JSON.stringify(this.listInput.reduce((total,{count,input}) => {
        total[count] = input;
        return total
      },{}))
      this.show = false
    },
    handleInput(e, item) {
      // e.target.value = (e.target.value.match(/^\d*(.?\d{0,1})/g)[0]) || null
      if (item.input > 100) {
        item.input = 100
        return
      }
      // if (item.input < 0) {
      //   item.input = 0.01
      //   return
      // }
      // item.input = (Math.floor(item.input * 100) / 100)
      item.input = item.input.match(/^\d*(.?\d{0,2})/g)[0]
    },
    ...mapActions({
      marketList: 'robot/marketList',
      robotCreate: 'robot/robotCreate',
      robotEdit: 'robot/robotEdit'
    }),
    onMarket() {
      if (this.formType === 'create') {
        this.marketPicker = true
      }
    },
    onSubmit() {
      let flag = false
      console.log(this.listInput)
      for (const key in this.listInput) {
        if (this.listInput[key].input !== '' || this.listInput[key].input > 0) {
          flag = true
        } else {
          this.$toast('补仓跌幅不能为空')
          flag = false
          return
        }
      }
      const {high_limit,low_limit}= this.robotPrice
      if(+this.price < low_limit){
         this.$toast('买入价不能低于最低买价')
          return
      }
      if(+this.price > high_limit){
         this.$toast('买入价不能高于最高买价')
          return
      }
      if (flag) {
        this.$toast.loading()
        const payload = {
          platform: this.platform,
          market_id: this.market_id,
          first_order_value: this.first_order_value,
          max_order_count: this.max_order_count,
          stop_profit_rate: this.stop_profit_rate,
          number: this.number,
          stop_profit_callback_rate: this.stop_profit_callback_rate,
          cover_rate: this.listInput,
          c_type: this.checked,
          type:2,
          // 补仓
          // cover_rate: this.cover_rate,
          cover_callback_rate: this.cover_callback_rate,
          sl_trigger_price: this.sl_trigger_price,
          price: this.price,
          direction: this.direction,
          cd_key: this.cd_key,
          recycle_status: this.recycle_status,
        }
        if (this.formType === 'edit') {
          payload.robot_id = this.robot_id
        }
        const promise =
        this.formType === 'create' ? this.robotCreate(payload) : this.robotEdit(payload)
        promise
          .then((res) => {
            this.$toast(res.msg)
            this.$router.back()
          })
          .catch(({ msg }) => this.$toast(msg))
      } else {
        this.$toast('补仓跌幅不能为空')
      }
    },
    onConfirm(value) {
      this.market = value.market_name
      this.market_id = value.id
      this.marketPicker = false
    },
    changePreset(index) {
      this.preset = index
      if (index === 1) {
        this.max_order_count = '6'
        this.stop_profit_rate = '1'
        this.stop_profit_callback_rate = '0.3'
        this.cover_rate = '1.8'
        this.cover_callback_rate = '0.3'
      } else if (index === 2) {
        this.max_order_count = '6'
        this.stop_profit_rate = '1.3'
        this.stop_profit_callback_rate = '0.3'
        this.cover_rate = '1.5'
        this.cover_callback_rate = '0.3'
      } else if (index === 3) {
        this.customStrateg = {
          max_order_count:this.max_order_count,
          stop_profit_rate:this.stop_profit_rate,
          number:this.number,
          stop_profit_callback_rate:this.stop_profit_callback_rate,
          cover_rate:this.cover_rate,
          cover_callback_rate:this.cover_callback_rate
        }
        const {max_order_count,stop_profit_rate,number,stop_profit_callback_rate,cover_rate,cover_callback_rate} = this.defaultStrategy;
        this.max_order_count = max_order_count || '17'
        this.stop_profit_rate = stop_profit_rate || '1.1'
        this.number = number || '10'
        this.stop_profit_callback_rate = stop_profit_callback_rate || '0.1'
        this.cover_rate = cover_rate || JSON.stringify(JSON.parse(cover_rate)) || '{"1":"1","2":"2","3":"3","4":"4","5":"5","6":"6","7":"7","8":"8","9":"9","10":"10","11":"13","12":"16","13":"19","14":"21","15":"26","16":"31","17":"41"}'
        this.cover_callback_rate = cover_callback_rate || '0.3'
      } else if (index === 4) {
        const {max_order_count,stop_profit_rate,number,stop_profit_callback_rate,cover_rate,cover_callback_rate} = this.customStrateg;
        for(var item in this.customStrateg){
          this[item] = this.customStrateg[item];
        }
        // this.max_order_count = max_order_count
        // this.stop_profit_rate = stop_profit_rate
        // this.stop_profit_callback_rate = stop_profit_callback_rate
        // this.cover_rate = cover_rate
        // this.number = number
        // this.cover_callback_rate = cover_callback_rate
      }
    },
    async getLimitPrice(){
      const {market_name} = this.queryData
      const {data:{data:[robotPrice]}}  = await this.$axios.$post(API.ROBOT_PRICE, {contract_code:market_name.replace('/','-')})
      this.robotPrice = robotPrice;
    },
    async getContractSize(){
      const {platform,market_name,type} = this.queryData;
      const {data} = await this.$axios.$post(API.MARKET_LIST, {
        platform,
        type:type === 1 ? 'spot' :'swap'
      })
     const current = data.filter(item => item.market_name === market_name)
     if(!current) return;
     this.contract_size = current[0].contract_size;
    },
    async getStrategy(){
      const {data} = await this.$axios.$post(API.ROBOT_STRATEGY, {type:this.queryData.type});
      this.defaultStrategy = data;
    }
  }
}
</script>

<style lang="less" scoped>
.title {
  padding: 10px 15px;
  font-size: 14px;line-height: 1;
  background: #fff;
}
.preset {
  padding: 0 10px 10px;
  display: flex;
  justify-content: space-around;
  background: #fff;

  .van-col {
    flex: 1;
    margin: 0 5px;
  }
  .van-button--primary{
    background: #1678FF;
  }
.van-cell {
  background: red;
}
}
.tips {
  padding: 10px 15px;
  font-size: 12px;
}
.setting{
  background: #1678FF;
  .van-button__content{
    color:#fff;
  }
}
.list_box {
  padding: 10px;
  box-sizing: border-box;
.van-button--info{
  width: 340px;
  height: 42px;
  color: #fff;
  font-style: 16px;
  line-height: 42px;
  text-align: center;
  margin:10px auto;
  border-radius: 20px;
}
  .listInput{
    overflow: hidden;
    li{
      padding: 0 10px;
      line-height: 20px;
      font-style: 12px;
      border-bottom: 1px solid #999;
      overflow: hidden;
      .list_span{
        float: left;
      }
      .list_input{
        border: none  !important;
        float: right !important;
      }
      .list_i{
        float: right !important;
       }
    }
  }
}
.box_{
    position: fixed;
    width: 100%;
    height: 100%;
    background: rgb(51,51,50,0.8);
    z-index: 11111111;
    top: 0;
    >div{
background: #fff;
    }
}
</style>
