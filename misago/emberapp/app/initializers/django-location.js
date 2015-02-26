import Ember from 'ember';

export function initialize(container, application) {
  application.register('location:django-location', Ember.HistoryLocation.extend({
    formatURL: function () {
      return this._super.apply(this, arguments).replace(/\/?$/, '/');
    }
  }));
}

export default {
  name: 'django-location',
  initialize: initialize
};
