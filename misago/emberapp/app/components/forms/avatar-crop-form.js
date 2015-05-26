import Ember from 'ember';

export default Ember.Component.extend({
  classNames: 'avatar-crop',
  cropit: Ember.inject.service('cropit'),

  isLoading: true,
  isCropping: false,

  secret: '',
  isNested: false,
  hash: null,

  crop: null,

  apiUrl: function() {
    return 'users/' + this.auth.get('user.id') + '/avatar';
  }.property(),

  finalSecret: function() {
    return this.get('secret') || this.get('options.crop_org.secret');
  }.property('secret', 'options.crop_org.secret'),

  finalHash: function() {
    return this.get('hash') || this.get('auth.user.avatar_hash');
  }.property('hash', 'auth.user.avatar_hash'),

  avatarSize: function() {
    if (this.get('isNested')) {
      return this.get('options.crop_tmp.size');
    } else {
      return this.get('options.crop_org.size');
    }
  }.property('options.crop_tmp.size', 'options.crop_org.size'),

  imagePath: function() {
    var src = Ember.$('base').attr('href') + 'user-avatar/';
    src += this.get('finalSecret') + ':' + this.get('finalHash') + '/';
    src += this.get('auth.user.id') + '.png';
    return src;
  }.property('finalSecret', 'finalHash', 'auth.user.id'),

  loadLibrary: function() {
    var self = this;
    this.get('cropit').load().then(function() {
      self.set('isLoading', false);

      Ember.run.scheduleOnce('afterRender', function() {
        // initialise cropper
        var $cropper = self.$('.image-cropper');

        $cropper.width(self.get('avatarSize'));
        $cropper.cropit({
          width: self.get('avatarSize'),
          height: self.get('avatarSize'),
          imageState: {
            src: self.get('imagePath')
          },
          onImageLoaded: function() {
            if (self.get('isNested')) {
              // center uploaded image
              var zoomLevel = $cropper.cropit('zoom');
              var imageSize = $cropper.cropit('imageSize');

              // is it wider than taller?
              if (imageSize.width > imageSize.height) {
                var displayedWidth = (imageSize.width * zoomLevel);
                var offsetX = (displayedWidth - self.get('avatarSize')) / -2;
                $cropper.cropit('offset', { x: offsetX, y: 0 });
              } else if (imageSize.width < imageSize.height) {
                var displayedHeight = (imageSize.height * zoomLevel);
                var offsetY = (displayedHeight - self.get('avatarSize')) / -2;
                $cropper.cropit('offset', { x: 0, y: offsetY });
              }
            } else {
              // use preserved crop
              var crop = self.get('options.crop_org.crop');
              if (crop) {
                $cropper.cropit('zoom', crop.zoom);
                $cropper.cropit('offset', { x: crop.x, y: crop.y });
              }
            }
          }
        });
      });
    });
  }.on('didInsertElement'),

  destroyCrop: function() {
    this.$('.image-cropper').cropit('disable');
  }.on('willDestroyElement'),

  actions: {
    crop: function() {
      if (this.get('isCropping')) { return; }
      this.set('isCropping', true);

      var opName = 'crop_org';
      if (this.get('isNested')) {
        opName = 'crop_tmp';
      }

      var $cropper = this.$('.image-cropper');

      var crop = {
        'offset': $cropper.cropit('offset'),
        'zoom': $cropper.cropit('zoom')
      };

      var self = this;
      this.ajax.post(this.get('apiUrl'), {
        'avatar': opName,
        'crop': crop
      }).then(function(data) {
        if (self.isDestroyed) { return; }
        self.toast.success(data.detail);
        self.get('options').setProperties(data.options);
        self.set('auth.user.avatar_hash', data.avatar_hash);
        self.set('activeForm', 'select-avatar-type-form');
      }, function(jhXHR) {
        if (self.isDestroyed) { return; }
        self.set('isCropping', false);
        if (jhXHR.status === 400) {
          self.toast.error(jhXHR.responseJSON.detail);
        } else {
          self.toast.apiError(jhXHR);
        }
      }).finally(function() {
        if (self.isDestroyed) { return; }
      });
    },

    cancel: function() {
      this.set('activeForm', 'select-avatar-type-form');
    }
  }
});
