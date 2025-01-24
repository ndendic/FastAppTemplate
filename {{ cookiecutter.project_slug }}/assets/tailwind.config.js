const colors = require('tailwindcss/colors')

/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: 'selector',
    content: ["./**/*.py"],
    theme: {
      extend: {
        colors: {
          base: {
            light: colors.gray[50],
            dark: colors.gray[900],
          },
          content: {
            light: {
              primary: colors.gray[900],
              secondary: colors.gray[600],
            },
            dark: {
              primary: colors.gray[50],
              secondary: colors.gray[300],
            }
          },
          surface: {
            light: colors.white,
            dark: colors.gray[800],
          },
          border: {
            light: colors.gray[200],
            dark: colors.gray[700],
          },
          error: {
            base: {
                light: colors.orange[50],    
                dark: colors.slate[950],     
            },
            accent: {
                light: colors.amber[500],    
                dark: colors.violet[400]     
            },
            button: {
                light: colors.amber[500],
                dark: colors.violet[400],
                hover: {
                    light: colors.amber[600],
                    dark: colors.violet[500]
                }
            }
        },
        },
        keyframes: {
          sparkle: {
            '0%, 100%': { opacity: '0.8' },
            '50%': { opacity: '0.4' }
          },
          wiggle: {
            '0%': { transform: 'translate(0, 0)' },
            '25%': { transform: 'translate(-2px, 1px)' },
            '50%': { transform: 'translate(2px, -1px)' },
            '75%': { transform: 'translate(-1px, -1px)' },
            '100%': { transform: 'translate(0, 0)' }
          }
        },
        animation: {
          sparkle: 'sparkle 3s ease-in-out infinite',
          wiggle: 'wiggle 2s ease-in-out infinite'
        }
      },
    },
    plugins: [],
}