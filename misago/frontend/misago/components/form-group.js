(function (Misago) {
  'use strict';

  var textFields = ['text', 'password', 'email'];

  var formGroup = {
    view: function(ctrl, kwargs) {
      var groupClass = '.form-group';
      var errors = null;
      var helpText = null;

      var controlType = kwargs.control.attrs.type;
      var controlId = kwargs.control.attrs.id;

      var feedbackId = controlId + '_feedback';
      var feedbackIcon = null;
      var showFeedbackIcon = null;

      var isValidated = kwargs.validationKey && kwargs.validation !== null;

      kwargs.control.attrs['aria-describedby'] = '';

      if (isValidated && kwargs.validation[kwargs.validationKey]) {
        showFeedbackIcon = textFields.indexOf(controlType) >= 0;
        kwargs.control.attrs['aria-describedby'] = feedbackId;

        if (kwargs.validation[kwargs.validationKey] === true) {
          groupClass += '.has-success';
          feedbackIcon = [
            m('span.material-icon.form-control-feedback',
              {
                'aria-hidden': 'true'
              },
              'check'
            ),
            m('span.sr-only#' + feedbackId, gettext("(success)"))
          ];
        } else {
          groupClass += '.has-error';
          errors = kwargs.validation[kwargs.validationKey];
          feedbackIcon = [
            m('span.material-icon.form-control-feedback',
              {
                'aria-hidden': 'true'
              },
              'clear'
            ),
            m('span.sr-only#' + feedbackId, gettext("(error)"))
          ];
        }
      }

      if (kwargs.helpText) {
        if (typeof kwargs.helpText === 'string' ||
            kwargs.helpText instanceof String) {
          helpText = m('p.help-block', kwargs.helpText);
        } else {
          helpText = kwargs.helpText;
        }
      }

      return m(groupClass, [
        m('label.control-label' + (kwargs.labelClass || ''),
          {
            for: kwargs.labelFor || controlId
          },
          kwargs.label + ':'
        ),
        m(kwargs.controlClass || '', [
          kwargs.control,
          showFeedbackIcon ? feedbackIcon : null,
          errors ? m('.help-block.errors', errors.map(function(item) {
            return m('p', item);
          })) : null,
          helpText
        ])
      ]);
    },
  };

  Misago.addService('component:form-group', function(_) {
    _.component('form-group', formGroup);
  },
  {
    after: 'components'
  });
} (Misago.prototype));
