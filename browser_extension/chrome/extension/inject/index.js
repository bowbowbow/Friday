import { init, toggle } from './app';

!(() => {
  const global = window.__fd = window.__fd || {};

  if (global.isInit) {
    toggle(global);
  } else {
    console.log('[GetSelector]: Injected');
    init(global);
    toggle(global);
  }
})();
