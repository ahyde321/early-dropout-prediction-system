/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./public/index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui'],
      },
      colors: {
        edps: {
          // Primary Colors
          primary: '#1A1F36',        // Deep navy for main text and headings
          primaryDark: '#0F1324',    // Darker navy for contrast
          primaryLight: '#2D3447',   // Lighter navy for secondary text
          
          // Action Colors
          action: '#2563EB',         // Bright blue for primary actions
          actionDark: '#1D4ED8',     // Darker blue for hover states
          actionLight: '#3B82F6',    // Lighter blue for secondary actions
          
          // Background Colors
          background: '#F8FAFC',     // Light gray for main background
          card: '#FFFFFF',           // White for cards and panels
          hover: '#F1F5F9',          // Light gray for hover states
          highlight: '#EFF6FF',      // Very light blue for highlights
          
          // Border Colors
          border: '#E2E8F0',         // Light gray for borders
          borderDark: '#CBD5E1',     // Slightly darker for emphasis
          
          // Text Colors
          textPrimary: '#1A1F36',    // Deep navy for main text
          textSecondary: '#64748B',  // Medium gray for secondary text
          textMuted: '#94A3B8',      // Light gray for muted text
          
          // Status Colors
          success: '#10B981',        // Green for success states
          successLight: '#D1FAE5',   // Light green for success backgrounds
          warning: '#F59E0B',        // Amber for warnings
          warningLight: '#FEF3C7',   // Light amber for warning backgrounds
          danger: '#EF4444',         // Red for errors and destructive actions
          dangerLight: '#FEE2E2',    // Light red for error backgrounds
          info: '#3B82F6',           // Blue for information
          infoLight: '#DBEAFE',      // Light blue for info backgrounds
          
          // Risk Level Colors
          lowRisk: '#10B981',        // Green for low risk
          lowRiskLight: '#D1FAE5',   // Light green for low risk backgrounds
          mediumRisk: '#F59E0B',     // Amber for medium risk
          mediumRiskLight: '#FEF3C7',// Light amber for medium risk backgrounds
          highRisk: '#EF4444',       // Red for high risk
          highRiskLight: '#FEE2E2',  // Light red for high risk backgrounds
          
          // Chart Colors
          chartPrimary: '#2563EB',   // Primary chart color
          chartSecondary: '#8B5CF6', // Secondary chart color
          chartTertiary: '#EC4899',  // Tertiary chart color
          
          // Gradients
          gradientPrimary: 'linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%)',
          gradientSuccess: 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
          gradientWarning: 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)',
          gradientDanger: 'linear-gradient(135deg, #EF4444 0%, #DC2626 100%)'
        }
      }
    }
  },
  plugins: [],
}
