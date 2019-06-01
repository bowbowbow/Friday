const CONTEXT_MENU_ID = 'FRIDAY';
let windowId = 0;

chrome.contextMenus.create({
  id: CONTEXT_MENU_ID,
  title: 'Friday',
  contexts: ['all'],
  documentUrlPatterns: [
    'http://*/*',
    'https://*/*',
  ],
  onclick: e => {
    if (e.menuItemId !== CONTEXT_MENU_ID) {
      return;
    }
    // copySelector(selectedTabId);
  },
});
