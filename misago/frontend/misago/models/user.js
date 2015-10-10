(function (Misago) {
  'use strict';

  var User = function(data) {
    this.id = data.id;

    this.isAuthenticated = !!this.id;
    this.isAnonymous = !this.isAuthenticated;

    this.slug = data.slug;
    this.username = data.username;

    this.acl = data.acl;
    this.rank = data.rank;
  };

  var deserializeUser = function(data) {
    if (data.joined_on) {
      data.joined_on = Misago.deserializeDatetime(data.joined_on);
    }

    return data;
  };

  Misago.addService('model:user', function(_) {
    _.models.add('user', {
      class: User,
      deserialize: deserializeUser
    });
  },
  {
    after: 'models'
  });
} (Misago.prototype));
