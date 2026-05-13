// Sidebar collapse + active item highlight + tab highlight
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

    // --- Active item highlight in sidebar (top-level items only) ---
    const sidebarItems = document.querySelectorAll('.sidebar-item');

    if (sidebarItems.length > 0) {
        sidebarItems.forEach(function (item) {
            item.addEventListener('click', function (event) {
                event.preventDefault();     // stop "#" jumping
                sidebarItems.forEach(function (i) {
                    i.classList.remove('active');
                });
                item.classList.add('active');
            });
        });
    }

    // --- Active tab highlight (CalendarEntry tabs) ---
    const tabs = document.querySelectorAll('.tab-item:not(.tab-add)'); // exclude '+' tab

    if (tabs.length > 0) {
        tabs.forEach(function (tab) {
            tab.addEventListener('click', function (event) {
                event.preventDefault();
                tabs.forEach(function (t) {
                    t.classList.remove('active');
                });
                tab.classList.add('active');
            });
        });
    }
});