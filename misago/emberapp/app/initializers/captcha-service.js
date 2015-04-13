import NoCaptcha from 'misago/services/nocaptcha';
import QACaptcha from 'misago/services/qacaptcha';
import ReCaptcha from 'misago/services/recaptcha';

export function initialize(container, application) {
  application.register('service:nocaptcha', NoCaptcha, { singleton: true });
  application.register('service:qacaptcha', QACaptcha, { singleton: true });
  application.register('service:recaptcha', ReCaptcha, { singleton: true });

  application.inject('service:recaptcha', 'settings', 'misago:settings');
  application.inject('service:qacaptcha', 'store', 'store:main');

  var captchaType = container.lookup('misago:settings').captcha_type;
  application.inject('component', 'captcha', 'service:' + captchaType + 'captcha');
}

export default {
  name: 'captcha-service',
  after: 'misago-settings',
  initialize: initialize
};
