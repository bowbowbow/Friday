import { init, toggle } from './app';

!(() => {
  const global = window.__fd = window.__fd || {};

  console.log('[GetSelector]: Injected');
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('runtime onMessage :', message);
    const action = message.action;
    const data = message.data;

    if (action === 'init') {
      init(global);
      toggle(global);
    } else if (action === 'stop') {
      toggle(global);
    }
  });
})();
