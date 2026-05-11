// Sidebar collapse + active item highlight
document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const toggleButton = document.getElementById('sidebarToggle');

    // --- Collapse / expand sidebar ---
    if (sidebar && toggleButton) {
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

        // Initial icon state
        updateIcon();
    }

    // --- Active item highlight in sidebar ---
    const sidebarItems = document.querySelectorAll('.sidebar-item');

    if (sidebarItems.length > 0) {
        sidebarItems.forEach(function (item) {
            item.addEventListener('click', function (event) {
                // Prevent "#" from jumping to top
                event.preventDefault();

                // Remove active from all, then add to clicked one
                sidebarItems.forEach(function (i) {
                    i.classList.remove('active');
                });
                item.classList.add('active');
            });
        });
    }
});