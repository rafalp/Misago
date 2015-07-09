import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  model: function(params) {
    console.log(params);
    return { val: 'nope' };
  },

  actions: {
    didTransition: function() {
      this.set('title', {
        title: gettext('Most Active'),
        parent: gettext('Users')
      });
    }
  }
});
