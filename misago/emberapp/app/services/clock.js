import Ember from 'ember';
import config from '../config/environment';

export default Ember.Service.extend({
  tick: Ember.computed.oneWay('_tick').readOnly(),

  doTick: function () {
    var self = this;
    if (config.environment !== 'test') {
      // running this loop in tests will block promises resolution
      Ember.run.later(function () {
        self.toggleProperty('_tick');
      }, config.APP.tickFrequency);
    }
  }.observes('_tick').on('init'),

  _tick: false
});
