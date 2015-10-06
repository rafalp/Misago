(function (Misago) {
  'use strict';

  Misago.input = function(kwargs) {
    var options = {
      disabled: kwargs.disabled || false,
      placeholder: kwargs.placeholder || null,
      config: kwargs.config || null
    };

    var element = 'input';

    if (kwargs.id) {
      element += '#' + kwargs.id;
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
