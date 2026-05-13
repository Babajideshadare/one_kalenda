// Sidebar collapse + Calendar View entries collapse
document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const toggleButton = document.getElementById('sidebarToggle');

    // --- Collapse / expand whole sidebar ---
    if (sidebar && toggleButton) {
        function updateIcon() {
            if (sidebar.classList.contains('collapsed')) {
                toggleButton.textContent = '☰';
            } else {
                toggleButton.textContent = 'X';
            }
        }

        toggleButton.addEventListener('click', function () {
            sidebar.classList.toggle('collapsed');
            updateIcon();
        });

        updateIcon();
    }

    // --- Collapse / expand CalendarEntry list under Calendar View ---
    const entriesList = document.getElementById('calendarEntriesList');
    const entriesToggle = document.getElementById('calendarEntriesToggle');

    if (entriesList && entriesToggle) {
        entriesToggle.addEventListener('click', function () {
            entriesList.classList.toggle('collapsed');
        });
    }
});