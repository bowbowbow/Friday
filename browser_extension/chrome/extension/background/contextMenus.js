const CONTEXT_MENU_ID = 'FRIDAY';
let windowId = 0;

const addSelector = tabId =>
  chrome.tabs.executeScript(tabId, {
    code: 'window.__gs && window.__gs.addSelector()',
  });

chrome.contextMenus.create({
  id: CONTEXT_MENU_ID,
  title: 'Add this element to candidate',
  contexts: ['all'],
  documentUrlPatterns: [
    'http://*/*',
    'https://*/*',
  ],
  onclick: (e, tab) => {
    if (e.menuItemId !== CONTEXT_MENU_ID) {
      return;
    }
    addSelector(tab.id);
  },
});
