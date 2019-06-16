import $ from 'jquery';
import finder from '@medv/finder';
import _ from 'lodash';
import { addStyle } from './addStyle';
import { initMessage, showMessage, hideMessage } from './info';
import { copyToClipboard } from './clipboard';

const clearEl = el => el && el.classList.remove('gs_hover');

export const toggle = (global, power) => {
  const state = !global.state;
  global.state = state;
  const action = power ? 'addEventListener' : 'removeEventListener';
  document[action]('mouseover', global.selectElement);
  document[action]('mouseout', global.clearElDebounce);

  if (!power) {
    clearEl(global.selectedEl);
    global.copiedEl && global.copiedEl.classList.remove('gs_copied');
    hideMessage(global);
    $('.Friday').remove();
    $('.gs_copied').removeClass('gs_copied');
  }
};

export const init = (global, state) => {
  global.isInit = true;
  global.selectedEl = null;

  global.clearElDebounce = _.debounce(
    () => clearEl(global.selectedEl) && hideMessage(global),
    200,
  );

  const showSelected = (selector, tagId) => {
    const selectedEl$ = $(selector);
    const position = selectedEl$.offset();


    if (!position) {
      console.error('[There is no saved element] tagId :', tagId, ', selector :', selector);
      return;
    }

    $('body').append(`
<div class="Friday Friday-tooltip-${tagId}" style="position: absolute; left: ${position.left}px; top: ${position.top - 24}px; z-index: 2100000000;">
  <div class="Friday" style="position:relative;">
    <div class="Friday" style="position: relative; background-color: black; color: white; padding: 1px 5px; border-radius: 4px; font-size: 12px; font-weight: 400;">#${tagId}</div>
    <img class="Friday Friday-cancel-${tagId}" data-selector="${selector}" data-index="${tagId}" src="${chrome.extension.getURL('img/cancel.png')}" style="width: 19px; height: 19px; object-fit: cover; position: absolute; right: -22px; top: 1px; cursor: pointer;"/>
  </div>
</div>`);

    selectedEl$.addClass('gs_copied');

    $(`.Friday-cancel-${tagId}`).click(function() {
      const index = $(this).attr('data-index');
      const selector = $(this).attr('data-selector');

      $(selector).removeClass('gs_copied');
      $(`.Friday-tooltip-${index}`).remove();

      let selectors = state.selectors;

      const targetIndex = _.findIndex(selectors, { location: window.location.href, tagId });
      if (targetIndex >= 0) selectors.splice(targetIndex, 1);
      chrome.runtime.sendMessage({
        action: 'update_state',
        data: {
          state: {
            ...state,
            selectors,
          },
        },
      });
    });
  };

  let insertIndex = 0;
  $('.Friday').remove();
  $('.gs_copied').removeClass('.gs_copied');
  const selectors = state.selectors;
  const location = window.location.href;
  for (let i = 0; i < selectors.length; i++) {
    if (location === selectors[i].location) {
      showSelected(selectors[i].path, selectors[i].tagId);
    }
    insertIndex = Math.max(insertIndex, selectors[i].tagId);
  }

  global.selectElement = _.debounce(e => {
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

    insertIndex += 1;
    const tagId = insertIndex;
    const selectors = state.selectors;
    selectors.push({
      path: selector,
      location: window.location.href,
      tagId,
    });
    chrome.runtime.sendMessage({
      action: 'update_state',
      data: {
        state: {
          ...state,
          selectors,
        },
      },
    });
    showSelected(selector, tagId);
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
