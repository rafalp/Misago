Misago.Router.map(function() {
  this.resource('misago', { path: '/' });
});

Misago.Router.reopen({
  location: 'history'
});
