(function (Misago) {
  'use strict';

  var persistent = function(el, isInit, context) {
    context.retain = true;
  };

  var styles = [
    'progress-bar-danger',
    'progress-bar-warning',
    'progress-bar-warning',
    'progress-bar-primary',
    'progress-bar-success'
  ];

  var labels = [
    gettext('Entered password is very weak.'),
    gettext('Entered password is weak.'),
    gettext('Entered password is average.'),
    gettext('Entered password is strong.'),
    gettext('Entered password is very strong.')
  ];

  var passwordStrength = {
    view: function(ctrl, kwargs, _) {
      var score = _.zxcvbn.scorePassword(kwargs.password, kwargs.inputs);
      var options = {
        config: persistent,
        class: styles[score],
        style: "width: " + (20 + (20 * score)) + '%',
        'role': "progressbar",
        'aria-valuenow': score,
        'aria-valuemin': "0",
        'aria-valuemax': "4"
      };

      return m('.help-block.password-strength', {key: 'password-strength'}, [
        m('.progress',
          m('.progress-bar', options,
            m('span.sr-only', labels[score])
          )
        ),
        m('p.text-small', labels[score])
      ]);
    },
  };

  Misago.addService('component:password-strength', function(_) {
    _.component('password-strength', passwordStrength);
  },
  {
    after: 'components'
  });
} (Misago.prototype));
