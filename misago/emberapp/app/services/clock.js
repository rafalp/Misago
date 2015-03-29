import Ember from 'ember';
import ENV from '../config/environment';

export default Ember.Service.extend({
  availableIn: ['controllers'],

  tick: Ember.computed.oneWay('_tick').readOnly(),

  doTick: function () {
    var self = this;
    if (ENV.environment !== 'test') {
      // running this loop in tests will block promises resolution
      Ember.run.later(function () {
        self.toggleProperty('_tick');
      }, ENV.APP.TICK_FREQUENCY);
    }
  }.observes('_tick').on('init'),

  _tick: false
});
