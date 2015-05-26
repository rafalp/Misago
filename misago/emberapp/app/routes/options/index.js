import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  redirectToForm: function() {
    return this.transitionTo('options.forum');
  }.on('activate')
});
