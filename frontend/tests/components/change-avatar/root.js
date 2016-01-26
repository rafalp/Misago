import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ChangeAvatar, { ChangeAvatarError } from 'misago/components/change-avatar/root'; // jshint ignore:line
import misago from 'misago/index';
import * as testUtils from 'misago/utils/test-utils';

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

describe("Change Avatar", function() {
  beforeEach(function() {
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
    $.mockjax.clear();
  });

  it("loads successfully", function(done) {
    $.mockjax({
      url: '/test-api/users/123/avatar/',
      status: 200,
      responseText: apiResponse
    });

    /* jshint ignore:start */
    testUtils.render(<ChangeAvatar user={misago.get('user')} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .modal-change-avatar', function() {
      assert.ok(true, "component renders");
      done();
    });
  });

  it("handles disconnection", function(done) {
    $.mockjax({
      url: '/test-api/users/123/avatar/',
      isTimeout: true
    });

    /* jshint ignore:start */
    testUtils.render(<ChangeAvatar user={misago.get('user')} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .modal-message', function() {
      assert.equal(
        $('#test-mount .modal-message p.lead').text().trim(),
        "Lost connection with application.",
        "component renders error");
      done();
    });
  });

  it("handles rejection", function(done) {
    $.mockjax({
      url: '/test-api/users/123/avatar/',
      status: 400,
      responseText: {
        detail: "I can't let you do this Dave."
      }
    });

    /* jshint ignore:start */
    testUtils.render(<ChangeAvatar user={misago.get('user')} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .modal-message', function() {
      assert.equal(
        $('#test-mount .modal-message p.lead').text().trim(),
        "I can't let you do this Dave.",
        "component renders error");
      done();
    });
  });

  it("handles rejection with reason", function(done) {
    $.mockjax({
      url: '/test-api/users/123/avatar/',
      status: 400,
      responseText: {
        detail: "Reasonable error.",
        reason: "<p class=\"reason\">I am the reason.</p>"
      }
    });

    /* jshint ignore:start */
    testUtils.render(<ChangeAvatar user={misago.get('user')} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .modal-message', function() {
      assert.equal(
        $('#test-mount .modal-message p.lead').text().trim(),
        "Reasonable error.",
        "component renders error");

      assert.equal(
        $('#test-mount .modal-message p.reason').text().trim(),
        "I am the reason.",
        "component renders html reason");
      done();
    });
  });

  it("showError callback works", function(done) {
    $.mockjax({
      url: '/test-api/users/123/avatar/',
      status: 200,
      responseText: apiResponse
    });

    let component = null;
    /* jshint ignore:start */
    component = testUtils.render(<ChangeAvatar user={misago.get('user')} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .modal-avatar-index', function() {
      component.showError({
        detail: "Callbacked error!",
        reason: "<p class=\"reason\">Callbacked html reason.</p>"
      });
    });

    testUtils.onElement('#test-mount .modal-message p.reason', function() {
      assert.equal(
        $('#test-mount .modal-message p.lead').text().trim(),
        "Callbacked error!",
        "component renders callbacked error message");

      assert.equal(
        $('#test-mount .modal-message p.reason').text().trim(),
        "Callbacked html reason.",
        "component renders callbacked html reason");
      done();
    });
  });

  it("switches to gallery and back", function(done) {
    $.mockjax({
      url: '/test-api/users/123/avatar/',
      status: 200,
      responseText: apiResponse
    });

    /* jshint ignore:start */
    testUtils.render(<ChangeAvatar user={misago.get('user')} />);
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .btn-avatar-gallery', function() {
      testUtils.simulateClick('#test-mount .btn-avatar-gallery');
    });

    testUtils.onElement('#test-mount .modal-avatar-gallery', function() {
      assert.ok($('#test-mount .modal-avatar-gallery').length,
        "gallery was displayed via showGallery");

      testUtils.simulateClick('#test-mount .modal-footer .btn-default');

      testUtils.onElement('#test-mount .modal-avatar-index', function() {
        assert.ok(true, 'returned to index via showIndex');
        done();
      });
    });
  });
});

describe("Change Avatar Error", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it('renders with message', function() {
    /* jshint ignore:start */
    testUtils.render(<ChangeAvatarError message="Lorem ipsum dolor met." />);
    /* jshint ignore:end */

    let element = $('#test-mount .modal-body');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('p.lead').text().trim(), "Lorem ipsum dolor met.",
      "avatar change error renders message");
  });

  it('renders with html reason', function() {
    /* jshint ignore:start */
    let reason = "<p class=\"reason\">Here's the reason!</p>";
    testUtils.render(
      <ChangeAvatarError message="Lorem ipsum dolor met."
                         reason={reason} />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .modal-body');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('p.lead').text().trim(), "Lorem ipsum dolor met.",
      "avatar change error renders message");
    assert.equal(element.find('p.reason').text().trim(), "Here's the reason!",
      "avatar change error renders reason html");
  });
});