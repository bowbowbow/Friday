const CONTEXT_MENU_ID = 'FRIDAY';

const addSelector = tabId =>
  chrome.tabs.executeScript(tabId, {
    code: 'window.__fd && window.__fd.addSelector()',
  });

chrome.contextMenus.create({
  id: CONTEXT_MENU_ID,
  title: 'Add this element',
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
