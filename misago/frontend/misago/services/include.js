(function (Misago) {
  'use strict';

  var include = function(script, remote) {
    if (!remote) {
      script = this.context.STATIC_URL + script;
    }

    $.ajax({
      url: script,
      cache: true,
      dataType: 'script'
    });
  };

  Misago.addService('include', function(_) {
    _.include = include;
  },
  {
    after: 'conf'
  });
}(Misago.prototype));
