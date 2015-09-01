/* global grecaptcha */
import FormRow from 'misago/components/form-row';

export default FormRow.extend({
  classNames: ['form-recaptcha'],

  renderWidget: function() {
    grecaptcha.render('g-captcha', {
      'sitekey': this.get('settings.recaptcha_site_key')
    });
  }.on('didInsertElement')
});
