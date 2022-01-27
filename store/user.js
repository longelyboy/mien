import { tokenStorage } from '@/utils/storage'
import API from '@/constants/api'

export const state = () => ({
  logged: false,
  token: '',
  userInfo: {},
  authInfo: []
})

export const mutations = {
  SET_USER_INFO (state, data) {
    state.userInfo = data
  },
  SET_USER_TOKEN (state, data) {
    state.token = data
  },
  SET_LOGGED (state, data) {
    state.logged = data
  },
  SET_AUTH_INFO (state, data) {
    state.authInfo = data
  }
}

export const actions = {
  async login ({ commit }, params) {
    const res = await this.$axios.$post(
      params[0] === 1 ? API.LOGIN : API.CODE_LOGIN,
      params[1]
    )
    const data = res.data
    tokenStorage.set(data.token)
    commit('SET_USER_INFO', data.user)
    commit('SET_USER_TOKEN', data.token)
    commit('SET_LOGGED', true)
    return res
  },
  async logOut ({ commit }) {
    await tokenStorage.remove()
    commit('SET_USER_INFO', {})
    commit('SET_USER_TOKEN', '')
    // commit('SET_LANG', 'hk')
    commit('SET_LOGGED', false)
  },
  async getCode (context, param) {
    return await this.$axios.$post(API.SEND_VERIFICATION_CODE, { username: param })
  },
  async register ({ commit }, params) {
    return await this.$axios.$post(API.REGISTER, params)
  },
  async getUserInfo ({ commit }) {
    const { data } = await this.$axios.$get(API.USER_INFO)
    commit('SET_USER_INFO', data)
    commit('SET_LOGGED', true)
  },
  async editUserInfo ({ commit }, params) {
    const data = await this.$axios.$post(API.USER_INFO, params)
    return data
  },
  async bindPhone ({ commit }, params) {
    return await this.$axios.$post(API.BIND_PHONE, params)
  },
  async bindEmail ({ commit }, params) {
    return await this.$axios.$post(API.BIND_EMAIL, params)
  },
  async forgetPwd ({ commit }, params) {
    return await this.$axios.$post(API.RESET_PWD, params)
  },
  async changePwd ({ commit }, params) {
    return await this.$axios.$post(API.CHANGE_PWD, params)
  },
  async addPayPwd ({ commit }, params) {
    return await this.$axios.$post(API.ADD_PAY_PWD, params)
  },
  async changePayPwd ({ commit }, params) {
    return await this.$axios.$post(API.CHANGE_PAY_PWD, params)
  },
  async forgetPayPwd ({ commit }, params) {
    return await this.$axios.$post(API.FORGET_PAY_PWD, params)
  },
  async invitationInfo ({ commit }) {
    return await this.$axios.$post(API.INVITATION_INFO)
  },
  async invitationList ({ commit }) {
    return await this.$axios.$post(API.INVITATION_LIST)
  },
  async cdkeyList ({ commit }) {
    return await this.$axios.$post(API.CDKEY_LIST)
  },
  async cdkeyBuy ({ commit }, params) {
    return await this.$axios.$post(API.CDKEY_BUY, params)
  },
  async cdkeyActive ({ commit }, params) {
    return await this.$axios.$post(API.CDKEY_INPUT, params)
  },
  async getAuth ({ commit }, params) {
    const { data } = await this.$axios.$post(API.USER_AUTH, params)
    commit('SET_AUTH_INFO', data)
  },
  async addAuth ({ commit }, params) {
    return await this.$axios.$post(API.ADD_AUTH, params)
  },
  async showAuth ({ commit }, params) {
    return await this.$axios.$post(API.SHOW_AUTH, params)
  },
  async checkOpenGoogle ({ commit }, params) {
    return await this.$axios.$post(API.OPEN_CHECK_GOOGLE, params)
  },
  async checkConfirmGoogle ({ commit }, params) {
    return await this.$axios.$post(API.CONFIRM_CHECK_GOOGLE, params)
  },
  async checkCloseGoogle ({ commit }, params) {
    return await this.$axios.$post(API.CLOSE_CHECK_GOOGLE, params)
  },
  async openAuthLogin ({ commit }, params) {
    const res = await this.$axios.$post(API.OPEN_AUTH_LOGIN, params)
    const data = res.data
    tokenStorage.set(data.token)
    commit('SET_USER_TOKEN', data.token)
    return res
  },
  async changeLevel ({ commit }, params) {
    return await this.$axios.$post(API.INVITATION_LEVEL, params)
  },
  async getinvitationLevelList ({ commit }, params) {
    console.log(1)
    return await this.$axios.$get(API.INVITATION_LEVELLIST, params)
  }
}
