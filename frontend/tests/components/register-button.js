import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom'; // jshint ignore:line
import RegisterButton from 'misago/components/register-button'; // jshint ignore:line
import misago from 'misago/index';
import captcha from 'misago/services/captcha';
import modal from 'misago/services/modal';
import snackbar from 'misago/services/snackbar';
import zxcvbn from 'misago/services/zxcvbn';

let snackbarStore = null;

describe("RegisterButton", function() {
  beforeEach(function() {
    snackbarStore = window.snackbarStoreMock();
    snackbar.init(snackbarStore);
    window.initModal(modal);
    window.contextClear(misago);

    /* jshint ignore:start */
    ReactDOM.render(
      <RegisterButton />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */
  });

  afterEach(function() {
    delete window.zxcvbn;
    window.emptyTestContainers();
  });

  it('renders', function() {
    let element = $('#test-mount button');
    assert.ok(element.length, "component rendered");
  });

  it('alerts about closed registration', function(done) {
    window.misago._context = {
      SETTINGS: {
        account_activation: 'closed'
      }
    };

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "New registrations are currently disabled.",
        type: 'info'
      }, "valid alert is raised");
      done();
    });

    window.simulateClick('#test-mount button');
  });

  it('opens registration modal', function(done) {
    window.misago._context = {
      SETTINGS: {
        captcha_type: 'no',
        account_activation: 'none'
      }
    };

    captcha.init(misago, {}, {}, {});
    zxcvbn.init({
      include: function(file) {
        assert.equal(file, 'misago/js/zxcvbn.js', "zxcvbn.js is requested");
        window.setTimeout(function() {
          window.zxcvbn = function() {
            return 0;
          };
        }, 200);
      }
    });

    window.simulateClick('#test-mount button');

    window.onElement('#modal-mount .modal-register', function() {
      let element = $('#modal-mount .modal-register');
      assert.ok(element.length, "registration modal was opened");

      done();
    });
  });
});
