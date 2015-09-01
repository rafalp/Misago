import Ember from 'ember';
import { fileSize } from 'misago/helpers/file-size';
import { endsWith } from 'misago/utils/strings';

export default Ember.Component.extend({
  classNames: 'avatar-upload',

  isBusy: false,
  allowUpload: true,

  selectedImage: null,
  progress: 0,
  uploadHash: null,

  apiUrl: function() {
    return 'users/' + this.auth.get('user.id') + '/avatar';
  }.property(),

  setupInput: function() {
    var self = this;
    this.$('input').change(function() {
      self.uploadImage(Ember.$(this)[0].files[0]);
    });
  }.on('didInsertElement'),

  destroyInput: function() {
    this.$('input').off();
  }.on('willDestroyElement'),

  uploadImage: function(image) {
    if (this.isDestroyed || this.get('isBusy')) { return; }
    this.set('allowUpload', false);

    // validate file
    if (image.size > this.get('options.upload.limit')) {
      var msg = gettext('Selected file is too big. (%(filesize)s)');
      this.toast.warning(msg.replace('%(filesize)s', fileSize(image.size)));

      this.set('allowUpload', true);
      return;
    }

    var invalidTypeMsg = gettext('Selected file type is not supported.');
    if (this.get('options.upload.allowed_mime_types').indexOf(image.type) === -1) {
      this.toast.warning(invalidTypeMsg);
    }

    var isExtensionFound = false;

    var loweredFilename = image.name.toLowerCase();
    var extensions = this.get('options.upload.allowed_extensions');
    Ember.EnumerableUtils.forEach(extensions, function(extension) {
      if (endsWith(loweredFilename, extension.toLowerCase())) {
        isExtensionFound = true;
      }
    });

    if (!isExtensionFound) {
      this.toast.warning(invalidTypeMsg);

      this.set('allowUpload', true);
      return;
    }

    // begin upload!
    this.setProperties({
      'selectedImage': image,
      'isBusy': true,
      'progress': 0
    });

    var data = new FormData();
    data.append('avatar', 'upload');
    data.append('image', image);

    var self = this;
    Ember.run.scheduleOnce('afterRender', function() {
      if (self.isDestroyed) { return; }
      var reader = new FileReader();
      reader.onload = function(e) {
        self.$('img')[0].src = e.target.result;
      };
      reader.readAsDataURL(image);
    });

    self.ajax.post(self.get('apiUrl'), data, function(e) {
      if (self.isDestroyed) { return; }
      if (e.lengthComputable) {
        self.set('progress', Math.round((e.loaded * 100) / e.total));
      }
    }).then(function(data) {
      if (self.isDestroyed) { return; }
      self.toast.info(gettext("Your image was uploaded successfully."));
      self.set('uploadHash', data.detail);
      self.get('options').setProperties(data.options);
    }, function(jhXHR) {
      if (self.isDestroyed) { return; }

      self.setProperties({
        'allowUpload': true,
        'selectedImage': null,
        'progress': 0
      });

      if (jhXHR.status === 400) {
        self.toast.error(jhXHR.responseJSON.detail);
      } else {
        self.toast.apiError(jhXHR);
      }
    }).finally(function() {
      if (self.isDestroyed) { return; }
      self.set('isBusy', false);
    });
  },

  extensions: function() {
    var finalList = [];

    var extensions = this.get('options.upload.allowed_extensions');
    Ember.EnumerableUtils.forEach(extensions, function(extension) {
      finalList.push(extension.substr(1));
    });

    return finalList.join(', ');
  }.property('options.upload.allowed_extensions'),

  progressBarWidth: function() {
    this.$('.progress-bar').css('width', this.get('progress') + '%');
  }.observes('progress'),

  actions: {
    selectFile: function() {
      // reset input
      this.$('input').wrap('<form>').closest('form').get(0).reset();
      this.$('input').unwrap();

      this.$('input').trigger('click');
    },

    cancel: function() {
      this.set('activeForm', 'select-avatar-type-form');
    }
  }
});
