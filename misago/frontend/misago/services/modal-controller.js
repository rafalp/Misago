(function (Misago) {
  'use strict';

  var Modal = function() {
    var self = this;

    var element = document.getElementById('modal-mount');

    this.destroy = function() {
      $(element).off();
      $('body').removeClass('modal-open');
      $('.modal-backdrop').remove();
    };

    // Open/close modal
    var modal = $(element).modal({show: false});
    this.open = false;

    modal.on('hidden.bs.modal', function () {
      if (self.open) {
        m.mount(element, null);
        this.open = false;
      }
    });

    this.show = function(component) {
      this.open = true;
      m.mount(element, component);
      modal.modal('show');
    };

    this.hide = function() {
      modal.modal('hide');
    };
  };

  Misago.addService('_modal', {
    factory: function() {
      return new Modal();
    },
    destroy: function(_) {
      _._modal.destroy();
    }
  },
  {
    before: 'mount-components'
  });
}(Misago.prototype));
