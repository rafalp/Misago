import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'img',
  classNames: 'user-avatar',
  attributeBindings: ['src', 'alt'],

  size: 100,

  src: function() {
    return '/user-avatar/' + this.get('size') + '/' + this.get('id') + '.png';
  }.property('id', 'size'),

  alt: function() {
    return '';
  }.property()
});
