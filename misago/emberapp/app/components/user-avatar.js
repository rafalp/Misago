import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'img',
  classNames: 'user-avatar',
  attributeBindings: ['src', 'alt', 'size:width', 'size:height'],

  size: 100,

  src: function() {
    var src = Ember.$('base').attr('href') + 'user-avatar/';

    if (this.get('user')) {
      if (this.get('prefix') && this.get('token')) {
        // special avatar source
        src += this.get('prefix') + ':' + this.get('token') + '/';
      } else {
        // just avatar size
        src += this.get('size') + '/';
      }
      return src + this.get('user') + '.png';
    } else {
      // just append avatar size to file to produce no-avatar placeholder
      return src + this.get('size') + '.png';
    }
  }.property('user', 'size'),

  alt: ''
});
