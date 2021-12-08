import { IS_STANDALONE } from '@/config/index'
export const CNY = 'CNY'
export const USD = 'USD'
export const CURRENCIES = {
  [CNY]: {
    name: CNY,
    label: '人民币',
    symbol: '¥'
  },
  [USD]: {
    name: USD,
    label: '美元',
    symbol: '$'
  }
}

export const THIRD_LOGIN_ENABLED = !IS_STANDALONE
const platform = [
  // {
  //   name: '火币',
  //   label: 'huobi',
  //   logo: require('~/assets/images/huobi.png')
  // },
  {
    name: 'OKEx',
    label: 'okex',
    logo: require('~/assets/images/okex.png')
  },
  {
    name: '币安',
    label: 'binance',
    logo: require('~/assets/images/binance.png')
  }
 
]

export const PLATFORM = platform
