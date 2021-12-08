// const { WEB_URL } = require('./config')
const { WEB_URL, DEPLOY_BASE } = require('./config')

let routerBase = '/'
const isProd = process.env.NODE_ENV === 'production'
if (isProd) {
  routerBase = DEPLOY_BASE
}
export default {
  // Disable server-side rendering (https://go.nuxtjs.dev/ssr-mode)
  ssr: false,
  loading: false,

  server: {
    port: 8888,
    host: '0.0.0.0'
  },

  router: {
    // mode: 'hash',
    // base: process.env.NODE_ENV === 'production' ? './' : '/'
    base: routerBase
  },

  // Target (https://go.nuxtjs.dev/config-target)
  target: 'static',

  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    title: 'MIEN',
    meta: [
      { charset: 'utf-8' },
      {
        name: 'viewport',
        content:
          'width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, viewport-fit=cover'
      },
      { hid: 'description', name: 'description', content: '' }
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }]
  },

  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: ['~/assets/styles/common.less'],

  styleResources: {
    less: ['~/assets/styles/variables.less']
  },

  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: [
    '~/plugins/vant',
    '~/plugins/vant',
    '~/plugins/router',
    '~/plugins/axios.client',
    '~/plugins/clipboard',
    '~/plugins/filters',
    '~/plugins/directives',
    '~/plugins/i18n.client',
    '~/plugins/luckdraw'

  ],

  axios: {
    baseURL: WEB_URL
  },

  // Auto import components (https://go.nuxtjs.dev/config-components)
  components: true,

  // Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
  buildModules: [],

  // Modules (https://go.nuxtjs.dev/config-modules)
  modules: ['@nuxtjs/style-resources', '@nuxtjs/axios'],

  // Build Configuration (https://go.nuxtjs.dev/config-build)
  build: {
    transpile: [/vant.*?less/],
    babel: {
      plugins: [
        [
          'import',
          {
            libraryName: 'vant',
            style: name => `${name}/style/less`
          },
          'vant'
        ]
      ]
    },
    loaders: {
      less: {
        lessOptions: {
          modifyVars: {
            hack: 'true; @import "./assets/styles/variables.less";'
          }
        }
      }
    }
  }
}
