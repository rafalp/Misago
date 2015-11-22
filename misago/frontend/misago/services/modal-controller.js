(function (Misago) {
  'use strict';

  var Modal = function(_) {
    var self = this;

    var element = document.getElementById('modal-mount');

    // Open/close modal
    var modal = $(element).modal({show: false});
    this.open = false;

    modal.on('hidden.bs.modal', function () {
      // m() object is stateful, so in tests we don't
      // unmount the components, as this breaks it
      if (self.open && !_.setup.test) {
        m.mount(element, null);
        this.open = false;
      }
    });

    this.show = function(component) {
      this.open = true;
      m.mount(document.getElementById('modal-mount'), component);
      $(element).modal('show');
    };

    this.hide = function() {
      modal.modal('hide');
    };
  };

  Misago.addService('_modal', function(_) {
    return new Modal(_);
  },
  {
    before: 'mount-components'
  });
}(Misago.prototype));
