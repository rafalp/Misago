import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'img',
  classNames: 'user-avatar',
  attributeBindings: ['src', 'alt', 'size:width', 'size:height'],

  size: 100,
  alt: '',

  src: function() {
    var src = Ember.$('base').attr('href') + 'user-avatar/';

    if (this.get('user.id')) {
      if (this.get('prefix') && this.get('token')) {
        // special avatar source
        src += this.get('prefix') + ':' + this.get('token') + '/';
      } else {
        // just avatar hash and size
        src += this.get('user.avatar_hash') + '/' + this.get('size') + '/';
      }
      return src + this.get('user.id') + '.png';
    } else {
      // just append avatar size to file to produce no-avatar placeholder
      return src + this.get('size') + '.png';
    }
  }.property('user.id', 'user.avatar_hash', 'size')
});
