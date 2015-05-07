import Ember from 'ember';

export default Ember.Component.extend({
  classNames: 'navbar-spacer',

  affixNavbar: function() {
    // take navbar's height in document
    this.$().height(this.$().height());

    // affix navbar
    this.$('.navbar').affix({
      offset: {
        top: this.$('.navbar').offset().top
      }
    });
  }.on('didInsertElement'),

  actions: {
    showModal: function(template, model) {
      this.modal.show(template, model);
    }
  }
});
