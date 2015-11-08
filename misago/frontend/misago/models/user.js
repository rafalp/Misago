(function (Misago) {
  'use strict';

  var User = function(data) {
    this.id = data.id;

    this.isAuthenticated = !!this.id;
    this.isAnonymous = !this.isAuthenticated;

    this.username = data.username;
    this.slug = data.slug;

    this.email = data.email;

    this.full_title = data.full_title;
    this.rank = data.rank;

    this.avatar_hash = data.avatar_hash;

    this.acl = data.acl;
  };

  var deserializeUser = function(data, models) {
    if (data.joined_on) {
      data.joined_on = Misago.deserializeDatetime(data.joined_on);
    }

    if (data.rank) {
      data.rank = models.deserialize('rank', data.rank);
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
    after: 'model:rank'
  });
} (Misago.prototype));
