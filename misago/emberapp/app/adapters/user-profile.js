import MisagoAdapter from 'misago/adapters/application';

export default MisagoAdapter.extend({
  pathForType: function(type) {
    return 'users';
  }
});
