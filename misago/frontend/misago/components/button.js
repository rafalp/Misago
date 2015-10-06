(function (Misago) {
  'use strict';

  var button = {
    view: function(ctrl, kwargs) {
      var options = {
        disabled: kwargs.disabled || kwargs.loading || false,
        config: kwargs.config || null,
        loading: kwargs.loading || false,
        type: kwargs.submit ? 'submit' : 'button',
        onclick: kwargs.onclick || null
      };

      var element = 'button[type="' + options.type + '"].btn';
      if (options.loading) {
        element += '.btn-loading';
      }

      if (kwargs.id) {
        element += '#' + kwargs.id;
      }

      element += (kwargs.class || '');

      var label = kwargs.label;
      if (options.loading) {
        label = [
          label,
          m('.loader-compact', [
            m('.bounce1'),
            m('.bounce2'),
            m('.bounce3')
          ])
        ];
      }

      return m(element, options, label);
    },
  };

  Misago.addService('component:button', {
    factory: function(_) {
      _.component('button', button);
    },
    after: 'components'
  });
} (Misago.prototype));
