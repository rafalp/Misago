import Ember from 'ember';

export default Ember.Component.extend({
  _service: Ember.inject.service('modal'),

  classNames: ['modal', 'fade'],

  attributeBindings: ['tabindex', 'role', 'aria-labelledby', 'aria-hidden'],
  tabindex: '-1',
  role: 'dialog',
  'aria-labelledby': 'appModalLabel',
  'aria-hidden': 'true',

  modalComponent: Ember.computed.alias('_service.activeComponent'),
  modalModel: Ember.computed.alias('_service.activeModel')
});
