import { init, toggle } from './app';

!(() => {
  const global = window.__fd = window.__fd || {};
  console.log('[GetSelector]: Injected');

  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('runtime onMessage :', message);
    const action = message.action;
    const data = message.data;

    if (action === 'init_state') {
      if (data.state.power) {
        init(global, data.state);
        toggle(global, true);
      } else {
        toggle(global, false);
      }
    }
    sendResponse();
  });
})();
