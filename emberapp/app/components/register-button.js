import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'button',

  attributeBindings: ['type'],
  type: 'button',

  modalState: Ember.inject.service('registration-modal'),

  click: function() {
    this.modal.show(this.get('modalState.template'));
  }
});
