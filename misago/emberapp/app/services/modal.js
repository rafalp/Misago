import Ember from 'ember';

export default Ember.Service.extend({
  _modal: null,

  render: function(template, model) {
    this.container.lookup('route:application').render('modals.' + template, {
      into: 'application',
      outlet: 'modal',
      model: model || null
    });
  },

  disconnect: function() {
    this.container.lookup('route:application').disconnectOutlet({
      outlet: 'modal',
      parentView: 'application'
    });
  },

  _setupModal: function() {
    var modal = null;

    modal = Ember.$('#appModal').modal({show: false});

    modal.on('shown.bs.modal', function () {
      Ember.$('#appModal').focus();
    });

    var self = this;
    modal.on('hidden.bs.modal', function() {
      self.disconnect();
    });

    this.set('_modal', modal);
  },

  show: function(template, model) {
    if (!this.get('_modal')) {
      this._setupModal();
    }

    this.render(template, model);

    Ember.$('#appModal').modal('show');
  },

  hide: function() {
    Ember.$('#appModal').modal('hide');
  }
});
