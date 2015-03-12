import Ember from 'ember';
import ENV from '../config/environment';

var HIDE_ANIMATION_LENGTH = 200;

export default Ember.Service.extend({
  id: null,
  type: null,
  message: null,
  isVisible: false,

  isInfo: Ember.computed.equal('type', 'info'),
  isSuccess: Ember.computed.equal('type', 'success'),
  isWarning: Ember.computed.equal('type', 'warning'),
  isError: Ember.computed.equal('type', 'error'),

  _showToast: function(type, message) {
    var toastId = this.incrementProperty('id');
    this.set('type', type);
    this.set('message', message);
    this.set('isVisible', true);

    var self = this;
    Ember.run.later(function () {
      if (self.get('id') === toastId) {
        self.set('isVisible', false);
      }
    }, ENV.APP.TOAST_BASE_DISPLAY_TIME + (message.length * 110));
  },

  _setToast: function(type, message) {
    var self = this;

    if (this.get('isVisible')) {
      this.set('isVisible', false);
      Ember.run.later(function () {
        self._showToast(type, message);
      }, HIDE_ANIMATION_LENGTH);
    } else {
      this._showToast(type, message);
    }
  },

  // Public api

  info: function(message) {
    this._setToast('info', message);
  },

  success: function(message) {
    this._setToast('success', message);
  },

  warning: function(message) {
    this._setToast('warning', message);
  },

  error: function(message) {
    this._setToast('error', message);
  }
});
