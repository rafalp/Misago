import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'button',

  attributeBindings: ['type'],
  type: 'button',
  classNames: ['btn', 'btn-outlined', 'btn-yes-no-switch'],
  classNameBindings: ['value:btn-success:btn-default'],

  yesLabel: gettext('Yes'),
  noLabel: gettext('No'),

  click: function() {
    this.toggleProperty('value');
  }
});
