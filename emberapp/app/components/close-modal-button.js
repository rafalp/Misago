import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'button',

  attributeBindings: ['type'],
  type: 'button',

  router: function() {
    return this.container.lookup('router:main');
  }.property(),

  click: function() {
    this.modal.hide();
    this.get('router').transitionTo(this.get('goto'));
  }
});
