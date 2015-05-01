import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  beforeModel: function() {
    this.auth.denyAuthenticated(gettext('Only guests can change forgotten password.'));
  }
});
