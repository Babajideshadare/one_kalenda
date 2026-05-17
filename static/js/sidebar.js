// Sidebar collapse + Calendar View entries collapse with remembered state
// + custom context menu (right click) for Rename/Delete on tabs and sidebar entries
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

    // --- Custom context menu (Rename/Delete) for tabs + sidebar entries ---
    const contextMenu = document.getElementById('entryContextMenu');
    let currentEntryId = null;

    function hideContextMenu() {
        if (contextMenu) {
            contextMenu.classList.add('hidden');
        }
        currentEntryId = null;
    }

    function showContextMenu(x, y) {
        if (!contextMenu) return;

        // Make sure the menu doesn't go off-screen
        const menuWidth = contextMenu.offsetWidth || 160;
        const menuHeight = contextMenu.offsetHeight || 80;
        const pageWidth = window.innerWidth;
        const pageHeight = window.innerHeight;

        let left = x;
        let top = y;

        if (left + menuWidth > pageWidth) {
            left = pageWidth - menuWidth - 8;
        }
        if (top + menuHeight > pageHeight) {
            top = pageHeight - menuHeight - 8;
        }

        contextMenu.style.left = left + 'px';
        contextMenu.style.top = top + 'px';
        contextMenu.classList.remove('hidden');
    }

    // Click on menu items
    if (contextMenu) {
        contextMenu.addEventListener('click', function (event) {
            const action = event.target.dataset.action;
            if (!action || !currentEntryId) {
                return;
            }

            if (action === 'rename') {
                window.location.href = `/entries/${currentEntryId}/rename/`;
            } else if (action === 'delete') {
                window.location.href = `/entries/${currentEntryId}/delete/`;
            }

            hideContextMenu();
        });
    }

    // Hide menu when clicking anywhere else
    document.addEventListener('click', function (event) {
        if (!contextMenu) return;
        if (!contextMenu.contains(event.target)) {
            hideContextMenu();
        }
    });

    // Also hide on scroll (so it doesn't hang in the wrong place)
    document.addEventListener('scroll', hideContextMenu, true);

    // --- Attach handlers to all tab items and sidebar entries ---
    const entryTargets = document.querySelectorAll(
        '.tab-item[data-entry-id], .sidebar-entry[data-entry-id]'
    );

    entryTargets.forEach(function (el) {
        const entryId = el.dataset.entryId;
        if (!entryId) return;

        // Double-click -> rename directly
        el.addEventListener('dblclick', function (event) {
            event.preventDefault();
            window.location.href = `/entries/${entryId}/rename/`;
        });

        // Right-click -> show custom context menu
        el.addEventListener('contextmenu', function (event) {
            event.preventDefault();
            currentEntryId = entryId;
            showContextMenu(event.pageX, event.pageY);
        });
    });
});