import { readFileSync } from 'node:fs'

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@nuxt/image',
    '@nuxt/ui',
    '@nuxt/content',
    'nuxt-og-image',
  ],

  app: {
    baseURL: '/guilt/'
  },

  devtools: {
    enabled: true
  },

  css: [
    '~/assets/css/main.css',
    'katex/dist/katex.min.css' 
  ],

  content: {
    build: {
      markdown: {
        remarkPlugins: { 'remark-math': {} },
        rehypePlugins: { 'rehype-katex': { output: 'html' }},
        highlight: {
          theme: 'red',
          langs: [
            JSON.parse(readFileSync('./grammars/rhai.tmLanguage.json', 'utf-8'))
          ]
        },
        toc: {
          searchDepth: 1
        }
      }
    }
  },

  experimental: {
    asyncContext: true
  },

  compatibilityDate: '2024-07-11',

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  },

  icon: {
    provider: 'iconify'
  },
})
