import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

import { createVuetify } from 'vuetify'

// Та же ботаническая палитра, что на лендинге — единый бренд.
const microgreenTheme = {
  dark: false,
  colors: {
    'background': '#f6f3ea',
    'surface': '#fffdf7',
    'primary': '#1f3d2b',
    'secondary': '#5b7355',
    'accent': '#9bcf3f',
    'on-background': '#1c2419',
    'on-surface': '#1c2419',
    'on-primary': '#f6f3ea',
  },
}

export const vuetify = createVuetify({
  theme: {
    defaultTheme: 'microgreenTheme',
    themes: { microgreenTheme },
  },
  defaults: {
    VBtn: { rounded: 'lg', class: 'text-none' },
    VCard: { rounded: 'xl' },
    VTextField: { variant: 'outlined', density: 'comfortable' },
    VTextarea: { variant: 'outlined', density: 'comfortable' },
    VSelect: { variant: 'outlined', density: 'comfortable' },
  },
})
