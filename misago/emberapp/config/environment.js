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

      // Min time flash is displayed for (in ms)
      FLASH_MIN_DISPLAY_TIME: 4500
    }
  };

  if (environment === 'development') {
    // ENV.APP.LOG_RESOLVER = true;
    ENV.APP.LOG_ACTIVE_GENERATION = true;
    ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    ENV.APP.LOG_VIEW_LOOKUPS = true;

    ENV.contentSecurityPolicy = {
      'default-src': "'none'",
      'script-src': "'self' 'unsafe-inline' https://cdn.mxpnl.com http://localhost:8000", // Allow scripts from https://cdn.mxpnl.com and Django runserver
      'font-src': "'self' http://fonts.gstatic.com", // Allow fonts to be loaded from http://fonts.gstatic.com
      'connect-src': "'self' https://api.mixpanel.com http://localhost:8000", // Allow data (ajax/websocket) from api.mixpanel.com, custom-api.local and Django runserver
      'img-src': "'self'",
      'style-src': "'self' 'unsafe-inline' http://fonts.googleapis.com", // Allow inline styles and loaded CSS from http://fonts.googleapis.com
      'media-src': "'self'"
    }

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
    ENV.APP.FLASH_MIN_DISPLAY_TIME = 500;
  }

  if (environment === 'production') {
    ENV.locationType = 'django-location';
  }

  return ENV;
};
