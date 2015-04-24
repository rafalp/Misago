/* global grecaptcha */
import FormRow from 'misago/components/form-row';

export default FormRow.extend({
  classNames: ['form-re-captcha'],

  renderWidget: function() {
    grecaptcha.render('g-captcha', {
      'sitekey': settings.recaptcha_site_key
    });
  }.on('didInsertElement')
});
