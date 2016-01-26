import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ChangeAvatarIndex from 'misago/components/change-avatar/index'; // jshint ignore:line
import misago from 'misago/index';
import snackbar from 'misago/services/snackbar';
import * as testUtils from 'misago/utils/test-utils';

let snackbarStore = null;
let apiResponse = {
    "crop_tmp": false,
    "galleries": [
        {
            "images": [
                "avatars/Nature/arctic_fox.jpg",
                "avatars/Nature/baby_fox.jpg",
                "avatars/Nature/blackbird.jpg",
                "avatars/Nature/rabbit.jpg",
                "avatars/Nature/serval.jpg"
            ],
            "name": "Nature"
        },
        {
            "images": [
                "avatars/Space/andromeda.jpg",
                "avatars/Space/antennae_galaxies.jpg",
                "avatars/Space/barred_spiral_galaxy.jpg",
                "avatars/Space/messier_74.jpg",
                "avatars/Space/ngc_1672.jpg",
                "avatars/Space/ngc_4414.jpg"
            ],
            "name": "Space"
        }
    ],
    "crop_org": false,
    "upload": {
        "allowed_extensions": [
            ".gif",
            ".png",
            ".jpg",
            ".jpeg"
        ],
        "limit": 750000,
        "allowed_mime_types": [
            "image/gif",
            "image/jpeg",
            "image/png"
        ]
    },
    "generated": true,
    "gravatar": true
};

describe("Change Avatar Index", function() {
  beforeEach(function() {
    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);

    misago._context = {
      'user': {
        'id': 123,
        'avatar_hash': 'aabbccdd',
        'api_url': {
          'avatar': '/test-api/users/123/avatar/'
        }
      }
    };
  });

  afterEach(function() {
    testUtils.unmountComponents();
    testUtils.snackbarClear(snackbar);
    $.mockjax.clear();
  });

  it("renders", function(done) {
    /* jshint ignore:start */
    testUtils.render(
      <ChangeAvatarIndex user={misago.get('user')}
                         options={apiResponse} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .modal-avatar-index', function() {
      assert.ok(true, "component renders");
      done();
    });
  });

  it("renders without gravatar button", function(done) {
    /* jshint ignore:start */
    let amendedOptions = Object.assign({}, apiResponse, {gravatar: false});
    testUtils.render(
      <ChangeAvatarIndex user={misago.get('user')}
                         options={amendedOptions} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .modal-avatar-index', function() {
      assert.ok(!$('#test-mount .btn-avatar-gravatar').length,
        "gravatar option is hidden");
      done();
    });
  });

  it("renders without gallery button", function(done) {
    /* jshint ignore:start */
    let amendedOptions = Object.assign({}, apiResponse, {galleries: false});
    testUtils.render(
      <ChangeAvatarIndex user={misago.get('user')}
                         options={amendedOptions} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .modal-avatar-index', function() {
      assert.ok(!$('#test-mount .btn-avatar-gallery').length,
        "gallery option is hidden");
      done();
    });
  });

  it("shows alert with error on rejection", function(done) {
    $.mockjax({
      url: '/test-api/users/123/avatar/',
      status: 400,
      responseText: {
        detail: "You can't change avatar at the moment!"
      }
    });

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "You can't change avatar at the moment!",
        type: 'error'
      }, "valid message was shown");
      done();
    });

    /* jshint ignore:start */
    testUtils.render(
      <ChangeAvatarIndex user={misago.get('user')}
                         options={apiResponse} />
    );
    /* jshint ignore:end */

    testUtils.simulateClick('#test-mount .btn-avatar-gravatar');
  });

  it("calls error callback on backend error", function(done) { // jshint ignore:line
    $.mockjax({
      url: '/test-api/users/123/avatar/',
      status: 403,
      responseText: {
        detail: "You need to sign in to change avatar."
      }
    });

    /* jshint ignore:start */
    let showError = function(error) {
      assert.equal(error.detail, "You need to sign in to change avatar.",
        "callback was called with backend error message");
      done();
    };

    testUtils.render(
      <ChangeAvatarIndex user={misago.get('user')}
                         options={apiResponse}
                         showError={showError} />
    );
    /* jshint ignore:end */

    testUtils.simulateClick('#test-mount .btn-avatar-gravatar');
  });

  it("changes avatar to generated one successfully", function(done) { // jshint ignore:line
    $.mockjax({
      url: '/test-api/users/123/avatar/',
      status: 200,
      responseText: {
        detail: "Generated avataru set!",
        avatar_hash: 'n33wh44sh',
        options: apiResponse
      }
    });

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Generated avataru set!",
        type: 'success'
      }, "valid message was shown");
    });

    /* jshint ignore:start */
    let onComplete = function(avatarHash, options) {
      assert.equal(avatarHash, 'n33wh44sh', "new hash was passed to callback");
      assert.deepEqual(options, apiResponse, "new ops ware passed to callback");

      done();
    };

    testUtils.render(
      <ChangeAvatarIndex user={misago.get('user')}
                         options={apiResponse}
                         onComplete={onComplete} />
    );
    /* jshint ignore:end */

    testUtils.simulateClick('#test-mount .btn-avatar-generate');
  });

  it("changes avatar to gravatar successfully", function(done) { // jshint ignore:line
    $.mockjax({
      url: '/test-api/users/123/avatar/',
      status: 200,
      responseText: {
        detail: "Gravatar avataru set!",
        avatar_hash: 'n33wh44sh',
        options: apiResponse
      }
    });

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Gravatar avataru set!",
        type: 'success'
      }, "valid message was shown");
    });

    /* jshint ignore:start */
    let onComplete = function(avatarHash, options) {
      assert.equal(avatarHash, 'n33wh44sh', "new hash was passed to callback");
      assert.deepEqual(options, apiResponse, "new ops ware passed to callback");

      done();
    };

    testUtils.render(
      <ChangeAvatarIndex user={misago.get('user')}
                         options={apiResponse}
                         onComplete={onComplete} />
    );
    /* jshint ignore:end */

    testUtils.simulateClick('#test-mount .btn-avatar-gravatar');
  });
});