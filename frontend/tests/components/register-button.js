import assert from 'assert';
import React from 'react'; // jshint ignore:line
import RegisterButton from 'misago/components/register-button'; // jshint ignore:line
import misago from 'misago/index';
import captcha from 'misago/services/captcha';
import modal from 'misago/services/modal';
import snackbar from 'misago/services/snackbar';
import zxcvbn from 'misago/services/zxcvbn';
import * as testUtils from 'misago/utils/test-utils';

let snackbarStore = null;

describe("RegisterButton", function() {
  beforeEach(function() {
    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);
    testUtils.initModal(modal);
    testUtils.contextClear(misago);

    /* jshint ignore:start */
    testUtils.render(<RegisterButton />);
    /* jshint ignore:end */
  });

  afterEach(function() {
    delete window.zxcvbn;
    testUtils.emptyTestContainers();
  });

  it('renders', function() {
    let element = $('#test-mount button');
    assert.ok(element.length, "component rendered");
  });

  it('alerts about closed registration', function(done) {
    misago._context = {
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

    testUtils.simulateClick('#test-mount button');
  });

  it('opens registration modal', function(done) {
    misago._context = {
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

    testUtils.simulateClick('#test-mount button');

    testUtils.onElement('#modal-mount .modal-register', function() {
      let element = $('#modal-mount .modal-register');
      assert.ok(element.length, "registration modal was opened");

      done();
    });
  });
});
