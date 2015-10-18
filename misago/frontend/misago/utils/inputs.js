(function (Misago) {
  'use strict';

  function persistent(el, isInit, context) {
    context.retain = true;
  }

  Misago.input = function(kwargs) {
    var options = {
      disabled: kwargs.disabled || false,
      config: kwargs.config || persistent
    };

    if (kwargs.placeholder) {
      options.placeholder = kwargs.placeholder;
    }

    if (kwargs.autocomplete === false) {
      options.autocomplete = 'off';
    }

    var element = 'input';

    if (kwargs.id) {
      element += '#' + kwargs.id;
      options.key = 'field-' + kwargs.id;
    }

    element += '.form-control' + (kwargs.class || '');
    element += '[type="' + (kwargs.type || 'text') + '"]';

    if (kwargs.value) {
      options.value = kwargs.value();
      options.oninput = m.withAttr('value', kwargs.value);
    }

    return m(element, options);
  };
}(Misago.prototype));
