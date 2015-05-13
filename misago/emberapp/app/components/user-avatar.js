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
      // just avatar hash, size and user id
      src += this.get('user.avatar_hash') + '/' + this.get('size') + '/' + this.get('user.id') + '.png';
    } else {
      // just append avatar size to file to produce no-avatar placeholder
      src += this.get('size') + '.png';
    }

    return src;
  }.property('user.id', 'user.avatar_hash', 'size')
});
