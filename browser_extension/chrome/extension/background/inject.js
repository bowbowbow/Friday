import * as chromeAPI from '../../../src/utils/chromeAPI';
import { init, toggle } from '../inject/app';

function isInjected(tabId) {
  return chrome.tabs.executeScriptAsync(tabId, {
    code: `var injected = window.reactInjected;
      window.reactInjected = true;
      injected;`,
    runAt: 'document_start',
  });
}

function loadScript(name, tabId, cb) {
  if (process.env.NODE_ENV === 'production') {
    chrome.tabs.executeScript(tabId, { file: `/js/${name}.bundle.js`, runAt: 'document_end' }, cb);
  } else {
    // dev: async fetch bundle
    fetch(`http://localhost:3000/js/${name}.bundle.js`)
    .then(res => res.text())
    .then((fetchRes) => {
      // Load redux-devtools-extension inject bundle,
      // because inject script and page is in a different context
      const request = new XMLHttpRequest();
      request.open('GET', 'chrome-extension://einpenlebdkihfkcinalemmfijdcmabp/js/redux-devtools-extension.js');  // sync
      request.send();
      request.onload = () => {
        if (request.readyState === XMLHttpRequest.DONE && request.status === 200) {
          chrome.tabs.executeScript(tabId, { code: request.responseText, runAt: 'document_start' });
        }
      };
      chrome.tabs.executeScript(tabId, { code: fetchRes, runAt: 'document_end' }, cb);
    });
  }
}

chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (changeInfo.status !== 'loading') return;

  const result = await isInjected(tabId);
  if (chrome.runtime.lastError) return;

  if (!result[0]) {
    loadScript('inject', tabId, () => {
      console.log('load inject bundle success!');
      chromeAPI.getState().then((state) => {
        chromeAPI.sendInitState(state).then();
      });
    });
  } else {
    // for SPA web such as reactjs
    chromeAPI.getState().then((state) => {
      chromeAPI.sendInitState(state).then();
    });
  }
});

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  console.log('message :', message);
  const action = message.action;
  const data = message.data;

  if (action === 'update_state') {
    chromeAPI.saveState(data.state);
  }
  sendResponse();
});
