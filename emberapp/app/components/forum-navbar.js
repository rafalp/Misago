import Ember from 'ember';

export default Ember.Component.extend({
  classNames: 'navbar-spacer',

  affixNavbar: function() {
    // reserve navbar's height in document
    this.$().height(this.$().height());

    // affix navbar
    this.$('.navbar').affix({
      offset: {
        // workaround around bootstrap affix mishandling
        // elements with resting position on top of page
        top: this.$('.navbar').offset().top + 1
      }
    });
  }.on('didInsertElement')
});
