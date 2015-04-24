/* jshint node: true */

module.exports = function(environment) {
  var ENV = {
    modulePrefix: 'misago',
    environment: environment,
    baseURL: '/',
    locationType: 'auto',
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. 'with-controller': true
      }
    },

    contentSecurityPolicy: {
      'default-src': "'none'",
      'frame-src': "https://www.google.com/recaptcha/",
      'script-src': "'self' 'unsafe-inline' 'unsafe-eval' https://www.google.com/recaptcha/ https://apis.google.com/ https://www.gstatic.com/recaptcha/ https://cdn.mxpnl.com", // Allow scripts from https://cdn.mxpnl.com
      'font-src': "'self' http://fonts.gstatic.com", // Allow fonts to be loaded from http://fonts.gstatic.com
      'connect-src': "'self' https://api.mixpanel.com", // Allow data (ajax/websocket) from api.mixpanel.com, custom-api.local
      'img-src': "*",
      'style-src': "'self' 'unsafe-inline' http://fonts.googleapis.com", // Allow inline styles and loaded CSS from http://fonts.googleapis.com
      'media-src': "*"
    },

    APP: {
      // Here you can pass flags/options to your application instance
      // when it is created
      rootElement: '#main',

      // Django API
      API_HOST: '',
      API_NAMESPACE: 'api',
      API_ADD_TRAILING_SLASHES: true,

      // Misago ticks frequency (in ms, used for refreshing timestamps)
      TICK_FREQUENCY: 15000,

      // Toastings time
      TOAST_BASE_DISPLAY_TIME: 4000,
      TOAST_LENGTH_FACTOR: 110,
      TOAST_HIDE_ANIMATION_LENGTH: 200
    }
  };

  if (environment === 'development') {
    // ENV.APP.LOG_RESOLVER = true;
    ENV.APP.LOG_ACTIVE_GENERATION = true;
    ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    ENV.APP.LOG_VIEW_LOOKUPS = true;

    ENV.APP.TICK_FREQUENCY = 1000;
  }

  if (environment === 'test') {
    // Testem prefers this...
    ENV.baseURL = '/';
    ENV.locationType = 'none';

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = '#ember-testing';

    // Maintain api config
    ENV.APP.API_HOST = '';
    ENV.APP.API_NAMESPACE = 'api';
    ENV.APP.API_ADD_TRAILING_SLASHES = true;

    // Reduce toast display times for test runner
    ENV.APP.TOAST_BASE_DISPLAY_TIME = 200;
    ENV.APP.TOAST_LENGTH_FACTOR = 0;
  }

  if (environment === 'production') {
    ENV.locationType = 'django-location';
  }

  return ENV;
};
