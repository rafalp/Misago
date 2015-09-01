import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'button',

  attributeBindings: ['type'],
  type: 'button',

  click: function() {
    document.location.reload();
  }
});
