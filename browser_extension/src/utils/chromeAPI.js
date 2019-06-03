export function saveState(state) {
  chrome.storage.local.set({ state: JSON.stringify(state) });
}

export async function getState() {
  return new Promise((resolve) => {
    chrome.storage.local.get('state', (result) => {
      const state = result.state;
      resolve(state ? JSON.parse(state) : { selectors: [], power: true });
    });
  });
}

export async function sendInitState(state) {
  return new Promise((resolve) => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.tabs.sendMessage(tabs[0].id, {
        action: 'init_state',
        data: { state },
      }, (response) => {
        resolve(response);
      });
    });
  });
}
