import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  usingUrlName: true,

  model: function(params) {
    var urlName = this.getParsedUrlNameOr404(params.url_name);
    return this.store.find('user-profile', urlName.id);
  },

  unloadUserModel: function() {
    this.store.unloadAll('user-profile');
  }.on('deactivate')
});
