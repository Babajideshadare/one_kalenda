// Sidebar collapse + Calendar View entries collapse with remembered state
// + redirect to rename page on double/right click of tabs and sidebar entries
document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const toggleButton = document.getElementById('sidebarToggle');

    const entriesList = document.getElementById('calendarEntriesList');
    const entriesToggle = document.getElementById('calendarEntriesToggle');
    const STORAGE_KEY = 'calendarEntriesCollapsed';

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

    // --- Restore and toggle collapsed state for nested CalendarEntry list ---
    if (entriesList && entriesToggle) {
        const isCollapsed = localStorage.getItem(STORAGE_KEY) === 'true';
        if (isCollapsed) {
            entriesList.classList.add('collapsed');
        }

        entriesToggle.addEventListener('click', function () {
            entriesList.classList.toggle('collapsed');
            const nowCollapsed = entriesList.classList.contains('collapsed');
            localStorage.setItem(STORAGE_KEY, nowCollapsed.toString());
        });
    }

    // --- Rename on double/right click (tabs + sidebar entries) ---
    const renameTargets = document.querySelectorAll(
        '.tab-item[data-entry-id], .sidebar-entry[data-entry-id]'
    );

    renameTargets.forEach(function (el) {
        const entryId = el.dataset.entryId;
        if (!entryId) return;

        const goToRename = function () {
            window.location.href = `/entries/${entryId}/rename/`;
        };

        // Double-click
        el.addEventListener('dblclick', function (event) {
            event.preventDefault();
            goToRename();
        });

        // Right-click
        el.addEventListener('contextmenu', function (event) {
            event.preventDefault();
            goToRename();
        });
    });
});