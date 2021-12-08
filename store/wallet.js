import API from '@/constants/api'
import { SET_FUND_DATA } from '@/constants/mutation-types'

export const state = () => ({
  totalPrice: 0, // 总价值
  funds: {}
})
export const mutations = {
  [SET_FUND_DATA] (state, data) {
    state.totalPrice = data.total_price
    const ownedFunds = {}
    data.list.forEach((item) => {
      ownedFunds[item.coin_symbol] = item
    })
    state.funds = { ...state.funds, ...ownedFunds }
  }
}
export const actions = {
  async fundList ({ commit }, params) {
    const res = await this.$axios.$post(API.WALLET_LIST, params)
    commit(SET_FUND_DATA, res.data)
    return res
  },
  async integralList ({ commit }, params) {
    return await this.$axios.$post(API.Scorelog, params)
  },
  async accountGame ({ commit }, params) {
    return await this.$axios.$post(API.ACCOUT_Game, params)
  },
  async GamelogList ({ commit }, params) {
    return await this.$axios.$post(API.GamelogList, params)
  },

  async fundDetail ({ commit }, params) {
    return await this.$axios.$post(API.WALLET_DETAIL, params)
  },
  async withdraw ({ commit }, params) {
    return await this.$axios.$post(API.WALLET_WITHDRAW, params)
  },
  async billList ({ commit }, params) {
    return await this.$axios.$post(API.WALLET_BILL, params)
  },
  async walletAddr ({ commit }, params) {
    return await this.$axios.$post(API.WALLET_ADDR, params)
  },
  async balanceLog ({ commit }, params) {
    return await this.$axios.$post(API.BALANCE_LOG, params)
  },
  async balanceTransfer ({ commit }, params) {
    return await this.$axios.$post(API.BALANCE_TRANSFER, params)
  }
}
