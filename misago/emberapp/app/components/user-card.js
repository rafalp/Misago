import Ember from 'ember';

export default Ember.Component.extend({
  classNames: ['user-card'],
  classNameBindings: ['rankClass'],

  rankClass: function() {
    if (this.get('user.rank.css_class').length) {
      return 'user-card-' + this.get('user.rank.css_class');
    } else {
      return ''
    }
  }.property('user.rank.css_class')
});
