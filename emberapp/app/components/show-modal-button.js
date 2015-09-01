import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'button',

  attributeBindings: ['type'],
  type: 'button',

  _modal: Ember.inject.service('modal'),

  click: function() {
    this.get('_modal').show(this.get('modal'), this.get('model'));
  }
});
