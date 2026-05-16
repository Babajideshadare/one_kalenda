// Sidebar collapse + Calendar View entries collapse with remembered state
// + redirect to rename page on double/right click of entry name pill
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

    // --- Rename via double-click / right-click on entry name pill ---
    const entryNameDisplay = document.getElementById('entryNameDisplay');
    if (entryNameDisplay) {
        const entryId = entryNameDisplay.dataset.entryId;
        if (entryId) {
            const goToRename = function () {
                window.location.href = `/entries/${entryId}/rename/`;
            };

            // Double-click
            entryNameDisplay.addEventListener('dblclick', function () {
                goToRename();
            });

            // Right-click (context menu)
            entryNameDisplay.addEventListener('contextmenu', function (event) {
                event.preventDefault(); // prevent default context menu
                goToRename();
            });
        }
    }
});