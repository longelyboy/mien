
import VueRouter from 'vue-router'
import { tokenStorage } from '~/utils/storage'
export default ({ app }) => {
  app.router.beforeEach((to, from, next) => {
    if (!localStorage.getItem('LANG')) {
      localStorage.setItem('LANG', 'hk')
      app.i18n.locale = 'hk'
    }
    let transitionName = ''
    const toDepth = to.path.split('/').length
    const fromDepth = from.path.split('/').length
    if (toDepth > fromDepth) {
      transitionName = 'slide-left'
    } else if (toDepth < fromDepth) {
      transitionName = 'slide-right'
    } else {
      transitionName = 'page'
    }
    app.store.dispatch('setTransitionName', transitionName)

    if (!app.store.state.initInfo || !Object.keys(app.store.state.initInfo).length > 0) {
      app.store.dispatch('getInitInfo')
    }
    const accessToken = tokenStorage.get() || ''
    if (accessToken) {
      if (!app.store.state.user.logged) {
        app.store.dispatch('user/getUserInfo')
      }
      if (app.store.state.robot.robotList.length === 0) {
        app.store.dispatch('robot/robotList')
      }
    }
    next()
  })
}

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push (location) {
  return originalPush.call(this, location)
}
