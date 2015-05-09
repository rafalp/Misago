import Ember from 'ember';

export default Ember.Service.extend({
  _modal: null,
  activeComponent: 'empty-modal',
  activeModel: null,

  _setupModal: function() {
    var modal = null;

    modal = Ember.$('#appModal').modal({show: false});

    modal.on('shown.bs.modal', function () {
      Ember.$('#appModal').focus();
    });

    var self = this;
    modal.on('hidden.bs.modal', function() {
      self.setProperties({
        activeComponent: 'empty-modal',
        activeModel: null
      });
    });

    this.set('_modal', modal);
  },

  show: function(component, model) {
    if (!this.get('_modal')) {
      this._setupModal();
    }

    this.setProperties({
      activeComponent: component,
      activeModel: model
    });

    Ember.$('#appModal').modal('show');
  },

  hide: function() {
    Ember.$('#appModal').modal('hide');
  }
});
