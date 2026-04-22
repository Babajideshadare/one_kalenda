// Toggle sidebar fully hidden/visible and switch icon between X and ☰
document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const toggleButton = document.getElementById('sidebarToggle');

    if (!sidebar || !toggleButton) {
        return;
    }

    function updateIcon() {
        if (sidebar.classList.contains('collapsed')) {
            // Sidebar is hidden -> show menu icon
            toggleButton.textContent = '☰';
        } else {
            // Sidebar is visible -> show X (close icon)
            toggleButton.textContent = 'X';
        }
    }

    toggleButton.addEventListener('click', function () {
        sidebar.classList.toggle('collapsed');
        updateIcon();
    });

    // Set correct icon on initial load
    updateIcon();
});