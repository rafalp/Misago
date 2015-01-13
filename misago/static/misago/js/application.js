window.Misago = Ember.Application.create({
  rootElement: '#main'
});


Misago.ApplicationController = Ember.Controller.extend(MisagoPreloadStore.data);
