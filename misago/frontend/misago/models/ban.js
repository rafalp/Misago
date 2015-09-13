(function (Misago) {
  'use strict';

  Misago.Ban = function(data) {
    this.message = {
      html: data.message.html,
      plain: data.message.plain,
    };

    this.expires_on = data.expires_on;
  };

  Misago.Ban.deserialize = function(data) {
    data.expires_on = Misago.deserializeDatetime(data.expires_on);

    return new Misago.Ban(data);
  };
} (Misago.prototype));
