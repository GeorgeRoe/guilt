export default defineAppConfig({
  ui: {
    colors: {
      primary: 'red',
      neutral: 'neutral'
    },
    footer: {
      slots: {
        root: 'border-t border-default',
        left: 'text-sm text-muted'
      }
    }
  },
  seo: {
    siteName: 'GUILT'
  },
  header: {
    title: 'GUILT',
    to: '/',
    logo: {
      alt: '',
      light: '',
      dark: ''
    },
    search: true,
    colorMode: false,
    links: [{
      'icon': 'i-simple-icons-github',
      'to': 'https://github.com/GeorgeRoe/guilt',
      'target': '_blank',
      'aria-label': 'GitHub'
    }]
  },
  footer: {
    credits: `© GUILT ${new Date().getFullYear()}`,
    colorMode: false,
    links: [{
      'icon': 'i-simple-icons-github',
      'to': 'https://github.com/GeorgeRoe/guilt',
      'target': '_blank',
      'aria-label': 'Nuxt UI on GitHub'
    }]
  },
  toc: {
    title: 'Table of Contents',
  }
})
