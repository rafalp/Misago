(function () {
  'use strict';

  var persistent = function(el, isInit, context) {
    context.retain = true;
  };

  window.mockMount = function(elementId, componentName) {
    return m('#' + elementId, {
      config: persistent,

      'data-component-name': componentName
    }, '-');
  };
}());
