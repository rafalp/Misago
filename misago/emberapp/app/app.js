import Ember from 'ember';
import Resolver from 'ember/resolver';
import loadInitializers from 'ember/load-initializers';
import registerGettextHelpers from 'django-ember-gettext/lib/main';
import config from './config/environment';

Ember.MODEL_FACTORY_INJECTIONS = true;

var App = Ember.Application.extend({
  rootElement: config.rootElement,
  modulePrefix: config.modulePrefix,
  podModulePrefix: config.podModulePrefix,
  Resolver: Resolver
});

registerGettextHelpers();
loadInitializers(App, config.modulePrefix);

export default App;
