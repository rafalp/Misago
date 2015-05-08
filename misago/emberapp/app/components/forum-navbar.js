import Ember from 'ember';

export default Ember.Component.extend({
  classNames: 'navbar-spacer',

  affixNavbar: function() {
    // take navbar's height in document
    this.$().height(this.$().height());

    // affix navbar
    var offset = this.$('.navbar').offset().top;
    if (offset === 0) {
      // workaround around bootstrap affix mishandling elements
      // with resting position on top of page
      offset = 1;
    }

    this.$('.navbar').affix({
      offset: {
        top: offset
      }
    });
  }.on('didInsertElement')
});
