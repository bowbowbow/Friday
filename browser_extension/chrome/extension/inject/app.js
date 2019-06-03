import $ from 'jquery';
import finder from '@medv/finder';
import debounce from 'lodash/debounce';
import { addStyle } from './addStyle';
import { initMessage, showMessage, hideMessage } from './info';
import { copyToClipboard } from './clipboard';

const clearEl = el => el && el.classList.remove('gs_hover');

export const toggle = (global) => {
  const state = !global.state;
  global.state = state;
  const action = state ? 'addEventListener' : 'removeEventListener';
  document[action]('mouseover', global.selectElement);
  document[action]('mouseout', global.clearElDebounce);

  if (!state) {
    clearEl(global.selectedEl);
    global.copiedEl && global.copiedEl.classList.remove('gs_copied');
    hideMessage(global);
  }
};

let insertIndex = 0;
const showSelected = (selector) => {
  insertIndex += 1;
  const selectedEl$ = $(selector);
  const position = selectedEl$.offset();

  $('body').append(`
<div class="Friday Friday-tooltip-${insertIndex}" style="position: absolute; left: ${position.left}px; top: ${position.top - 24}px; z-index: 2100000000;">
  <div class="Friday" style="position:relative;">
    <div class="Friday" style="position: relative; background-color: black; color: white; padding: 1px 5px; border-radius: 4px; font-size: 12px; font-weight: 400;">FRIDAY#${insertIndex}</div>
    <img class="Friday Friday-cancel-${insertIndex}" data-selector="${selector}" data-index="${insertIndex}" src="${chrome.extension.getURL('img/cancel.png')}" style="width: 19px; height: 19px; object-fit: cover; position: absolute; right: -22px; top: 1px; cursor: pointer;"/>
  </div>
</div>`);

  selectedEl$.addClass('gs_copied');

  $(`.Friday-cancel-${insertIndex}`).click(function() {
    const index = $(this).attr('data-index');
    const selector = $(this).attr('data-selector');

    $(selector).removeClass('gs_copied');
    $(`.Friday-tooltip-${index}`).remove();
  });
};

export const init = (global, state) => {
  global.isInit = true;
  global.selectedEl = null;

  global.clearElDebounce = debounce(
    () => clearEl(global.selectedEl) && hideMessage(global),
    200,
  );

  const selectors = state.selectors;
  const location = window.location.pathname;
  for (let i = 0; i < selectors.length; i++) {
    if (location === selectors[i].location) {
      showSelected(selectors[i].path);
    }
  }

  global.selectElement = debounce(e => {
    if (global.selectedEl !== e.target) {
      clearEl(global.selectedEl);
    }
    global.selectedEl = e.target;
    const selectedEl = global.selectedEl;

    if (selectedEl.classList.value.indexOf('Friday') >= 0) return;
    selectedEl.classList.add('gs_hover');

    const name = selectedEl.nodeName.toLowerCase();
    const id = selectedEl.id ? '#' + selectedEl.id : '';
    const className = selectedEl.className.replace
      ? selectedEl.className
      .replace('gs_hover', '')
      .trim()
      .replace(/ /gi, '.')
      : '';
    const message = name + id + (className.length > 0 ? '.' + className : '');
    showMessage(global, message);
  }, 200);

  global.addSelector = () => {
    const { selectedEl } = global;
    if (!selectedEl) {
      return;
    }
    clearEl(selectedEl);
    const selector = finder(selectedEl);

    chrome.runtime.sendMessage({
      action: 'updateState',
      state: state,
    });

    showSelected(selector);
  };

  addStyle(`
    .gs_hover {
      background: repeating-linear-gradient( 135deg, rgba(225, 225, 226, 0.3), rgba(229, 229, 229, 0.3) 10px, rgba(173, 173, 173, 0.3) 10px, rgba(172, 172, 172, 0.3) 20px );
      box-shadow: inset 0px 0px 0px 1px #d7d7d7;
    }
    .gs_copied {
      background: repeating-linear-gradient( 135deg, rgba(183, 240, 200, 0.3), rgba(192, 231, 194, 0.3) 10px, rgba(124, 189, 126, 0.3) 10px, rgba(137, 180, 129, 0.3) 20px ) !important;
      box-shadow: inset 0px 0px 0px 1px #c4d9c2 !important;      
    }
  `);
  initMessage(global);
};
