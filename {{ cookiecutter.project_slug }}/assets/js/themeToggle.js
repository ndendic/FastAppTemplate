// Prevent FOUC (Flash of Unstyled Content)
(function() {
    // Check if theme is stored in localStorage or use system preference
    if (localStorage.theme === 'dark' || 
        (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
})();

// Theme toggle functionality
function updateTheme(isDark) {
    // Update dark mode class
    if (isDark) {
        document.documentElement.classList.add('dark');
        localStorage.theme = 'dark';
    } else {
        document.documentElement.classList.remove('dark');
        localStorage.theme = 'light';
    }
    
    // Update checkbox state if it exists
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.checked = isDark;
    }
}

// Initialize theme and set up listeners when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    
    // Initialize theme based on current class
    if (themeToggle) {
        themeToggle.checked = document.documentElement.classList.contains('dark');
        
        // Listen for toggle changes
        themeToggle.addEventListener('change', function() {
            updateTheme(this.checked);
        });
    }
    
    // Optional: Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!localStorage.theme) {  // Only update if user hasn't manually set theme
            updateTheme(e.matches);
        }
    });
});