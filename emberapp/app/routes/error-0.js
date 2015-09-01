import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  setTitle: function() {
    this.set('title', gettext('Connection lost'));
  }.on('activate')
});
