import Ember from 'ember';

export function initialize(container, application) {
  application.register('location:trailing-history', Ember.HistoryLocation.extend({
    formatURL: function () {
      return this._super.apply(this, arguments).replace(/\/?$/, '/');
    }
  }));
}

export default {
  name: 'trailing-slash',
  initialize: initialize
};
