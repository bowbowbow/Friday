export function saveState(state) {
  chrome.storage.local.set({ state: JSON.stringify(state) });
}

export async function getState() {
  return new Promise((resolve) => {
    chrome.storage.local.get('state', (result) => {
      const state = result.state;
      resolve(state ? JSON.parse(state) : { keywords: [], power: true });
    });
  });
}

export async function sendKeywords(keywords) {
  return new Promise((resolve) => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const tab = tabs[0];
      if (tab.url.indexOf('https://coinpan.com') === -1) return;
      chrome.tabs.sendMessage(tabs[0].id, {
        action: 'hide_keywords',
        data: { keywords },
      }, (response) => {
        resolve(response);
      });
    });
  });
}

// todos unmarked count
// function setBadge(todos) {
//   if (chrome.browserAction) {
//     const count = todos.filter(todo => !todo.marked).length;
//     chrome.browserAction.setBadgeText({ text: count > 0 ? count.toString() : '' });
//   }
// }
//
// export default function() {
//   return next => (reducer, initialState) => {
//     const store = next(reducer, initialState);
//     store.subscribe(() => {
//       const state = store.getState();
//       // saveState(state);
//       // setBadge(state.todos);
//     });
//     return store;
//   };
// }
