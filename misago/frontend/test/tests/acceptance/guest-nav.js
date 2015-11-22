(function () {
  'use strict';

  var app = null;

  var mockNavbar = {
    view: function() {
      return m('nav.navbar.navbar-misago.navbar-default.navbar-static-top',
        m('.container.navbar-full',
          mockMount('user-menu-mount', 'navbar:desktop:guest-nav')
        )
      );
    }
  };

  QUnit.acceptance("Guest Nav", {
    beforeEach: function() {
      m.mount(document.getElementById('component-mount'), mockNavbar);
      app = initTestMisago();
    },
    afterEach: function() {
      app.destroy();
    }
  });

  QUnit.test('menu opens sign-in modal', function(assert) {
    var done = assert.async();

    click('.nav-guest .btn-default');

    onElement('.modal-signin', function() {
      assert.ok(true, "sign-in modal was shown after pressing button.");
      done();
    });
  });

  QUnit.test('menu opens registration modal', function(assert) {
    var done = assert.async();

    click('.nav-guest .btn-primary');

    onElement('.modal-register', function() {
      assert.ok(true, "registration modal was shown after pressing button.");
      done();
    });
  });

  QUnit.test('menu alerts about registration being off', function(assert) {
    var done = assert.async();

    app.settings.account_activation = 'closed';

    click('.nav-guest .btn-primary');

    onElement('.alerts .alert-info', function() {
      assert.equal(getAlertMessage(),
        "New registrations are currently disabled.",
        "alert about registrations being off was displayed.");
      done();
    });
  });
}());
