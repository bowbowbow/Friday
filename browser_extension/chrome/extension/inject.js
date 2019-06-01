import $ from 'jquery';

console.log('inject.js is loaded');

// let beforeKeywords = [];
//
// chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
//   // console.log('[contents script] message :', message);
//   const action = message.action;
//   const data = message.data;
//
//   if (action === 'hide_keywords') {
//
//     const hideCount = {};
//     const keywords = data.keywords;
//
//     // console.log('beforeKeywords:', beforeKeywords, ', keywords:', keywords);
//
//     for (let i = 0; i < keywords.length; i++) {
//       const keyword = keywords[i];
//
//       hideCount[keyword] = 0;
//
//       const beforeKeywordIndex = beforeKeywords.indexOf(keyword);
//       if (beforeKeywordIndex >= 0) {
//         beforeKeywords.splice(beforeKeywordIndex, 1);
//       }
//
//       let elements = $(`a:contains("${keyword}")`).parent('li');
//       hideCount[keyword] += elements.length;
//       elements.hide();
//
//       elements = $(`td:contains("${keyword}")`).parent('tr');
//       hideCount[keyword] += elements.length;
//       elements.hide();
//     }
//
//     for (let i = 0; i < beforeKeywords.length; i++) {
//       const keyword = beforeKeywords[i];
//
//       $(`a:contains("${keyword}")`).parent('li').show();
//       $(`td:contains("${keyword}")`).parent('tr').show();
//     }
//
//     beforeKeywords = keywords;
//
//     sendResponse({hideCount});
//   }
// });

$.fn.extend({
  getPath: function() {
    var pathes = [];

    this.each(function(index, element) {
      var path, $node = $(element);

      while ($node.length) {
        var realNode = $node.get(0), name = realNode.localName;
        if (!name) {
          break;
        }

        name = name.toLowerCase();
        var parent = $node.parent();
        var sameTagSiblings = parent.children(name);

        if (sameTagSiblings.length > 1) {
          var allSiblings = parent.children();
          var index = allSiblings.index(realNode) + 1;
          if (index > 0) {
            name += ':nth-child(' + index + ')';
          }
        }

        path = name + (path ? ' > ' + path : '');
        $node = parent;
      }

      pathes.push(path);
    });

    return pathes.join(',');
  },
});

window.addEventListener('load', () => {
  const injectDOM = document.createElement('div');
  injectDOM.className = 'inject-react';
  document.body.appendChild(injectDOM);

  console.log('[Friday] inject contents script');

  const coloredElements = {};

  // je.css({'cursor': `url(${chrome.extension.getURL('img/sniper.png')}), default`})
  $('body').css({'cursor': `crosshair`});

  $('body').mouseover((e) => {
    const element = e.target;
    const je = $(element);
    const path = je.getPath();

    const beforeBackgroundColor = je.css('background-color');
    je.css('background-color', 'rgba(119,168,255, 0.1)');
    // je.css({'cursor': `crosshair`});

    coloredElements[path] = beforeBackgroundColor ? beforeBackgroundColor : 'transparent';

  }).mouseout((e) => {
    const element = e.target;
    const je = $(element);
    const path = je.getPath();

    if (path in coloredElements) {
      const beforeBackgroundColor = coloredElements[path];
      je.css('background-color', beforeBackgroundColor);
      delete coloredElements[path];
    }
  });
});
