/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./*.html'],
  theme: {
    extend: {
      colors: {
        brand: {
          50:  '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        // Action color — Brunson-style high-contrast orange for primary CTAs
        signal: {
          400: '#ff8c4d',
          500: '#ff6b1a',
          600: '#e85a0c',
        },
        dark: {
          800: '#1e293b',
          900: '#0f172a',
        },
      },
      fontFamily: {
        display: ['"Inter Display"', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
        body: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      keyframes: {
        'cta-pulse': {
          '0%, 100%': { boxShadow: '0 12px 32px rgba(255, 107, 26, 0.35), 0 0 0 0 rgba(255, 107, 26, 0.55)' },
          '50%':      { boxShadow: '0 18px 44px rgba(255, 107, 26, 0.55), 0 0 0 12px rgba(255, 107, 26, 0)' },
        },
        'fade-in-up': {
          '0%':   { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'proof-tick': {
          '0%':   { transform: 'translateY(110%)', opacity: '0' },
          '10%':  { transform: 'translateY(0)',    opacity: '1' },
          '85%':  { transform: 'translateY(0)',    opacity: '1' },
          '100%': { transform: 'translateY(-110%)', opacity: '0' },
        },
        'glow-subtle': {
          '0%, 100%': { opacity: '0.6' },
          '50%':      { opacity: '1' },
        },
        'slide-up': {
          '0%':   { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'scale-in': {
          '0%':   { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
      },
      animation: {
        'cta-pulse':   'cta-pulse 2.4s ease-in-out infinite',
        'fade-in-up':  'fade-in-up 0.4s ease-out both',
        'proof-tick':  'proof-tick 5s ease-in-out',
        'glow-subtle': 'glow-subtle 3s ease-in-out infinite',
        'slide-up':    'slide-up 0.5s ease-out both',
        'scale-in':    'scale-in 0.3s ease-out both',
      },
      transitionTimingFunction: {
        'bounce-in': 'cubic-bezier(0.34, 1.56, 0.64, 1)',
      },
    },
  },
}
