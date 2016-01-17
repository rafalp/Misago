import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ChangeAvatarGallery, { Gallery, GalleryItem } from 'misago/components/change-avatar/gallery'; // jshint ignore:line
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

describe("Change Avatar Gallery", function() {
  beforeEach(function() {
    snackbarStore = testUtils.snackbarStoreMock();
    snackbar.init(snackbarStore);

    misago._context = {
      'user': {
        'id': 123,
        'avatar_hash': 'aabbccdd',
        'avatar_api_url': '/test-api/users/123/avatar/'
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
      <ChangeAvatarGallery user={misago.get('user')}
                           options={apiResponse} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .modal-avatar-gallery', function() {
      assert.ok(true, "component renders");
      done();
    });
  });

  it("handles backend rejection", function(done) {
    $.mockjax({
      url: '/test-api/users/123/avatar/',
      status: 400,
      responseText: {
        detail: "Lol nope!"
      }
    });

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Lol nope!",
        type: 'error'
      }, "error message was shown");

      done();
    });

    let component = null;

    /* jshint ignore:start */
    component = testUtils.render(
      <ChangeAvatarGallery user={misago.get('user')}
                           options={apiResponse} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .btn-avatar', function() {
      testUtils.simulateClick('#test-mount .btn-avatar');
    });

    testUtils.onElement('#test-mount .avatar-selected', function() {
      assert.equal(component.state.selection, "avatars/Nature/arctic_fox.jpg",
        "avatar selection callback works");
      testUtils.simulateClick('#test-mount .btn-primary');
    });
  });

  it("handles backend error", function(done) { // jshint ignore:line
    $.mockjax({
      url: '/test-api/users/123/avatar/',
      status: 403,
      responseText: {
        detail: "Avatar can't be changed at this time!"
      }
    });

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Lol nope!",
        type: 'error'
      }, "error message was shown");

      done();
    });

    let component = null;

    /* jshint ignore:start */
    let showError = function(error) {
      assert.equal(error.detail, "Avatar can't be changed at this time!",
        "callback was called with backend error message");
      done()
    };

    component = testUtils.render(
      <ChangeAvatarGallery user={misago.get('user')}
                           options={apiResponse}
                           showError={showError} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .btn-avatar', function() {
      testUtils.simulateClick('#test-mount .btn-avatar');
    });

    testUtils.onElement('#test-mount .avatar-selected', function() {
      assert.equal(component.state.selection, "avatars/Nature/arctic_fox.jpg",
        "avatar selection callback works");
      testUtils.simulateClick('#test-mount .btn-primary');
    });
  });

  it("selects and submits avatar", function(done) { // jshint ignore:line
    $.mockjax({
      url: '/test-api/users/123/avatar/',
      status: 200,
      responseText: {
        detail: "Gallery avataru set!",
        avatar_hash: 'n33wh44sh',
        options: apiResponse
      }
    });

    snackbarStore.callback(function(message) {
      assert.deepEqual(message, {
        message: "Gallery avataru set!",
        type: 'success'
      }, "valid message was shown");
    });

    let component = null;

    /* jshint ignore:start */
    let onComplete = function(avatarHash, options) {
      assert.equal(avatarHash, 'n33wh44sh', "new hash was passed to callback");
      assert.deepEqual(options, apiResponse, "new ops ware passed to callback");

      done();
    }

    component = testUtils.render(
      <ChangeAvatarGallery user={misago.get('user')}
                           options={apiResponse}
                           onComplete={onComplete} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .btn-avatar', function() {
      testUtils.simulateClick('#test-mount .btn-avatar');
    });

    testUtils.onElement('#test-mount .avatar-selected', function() {
      assert.equal(component.state.selection, "avatars/Nature/arctic_fox.jpg",
        "avatar selection callback works");
      testUtils.simulateClick('#test-mount .btn-primary');
    });
  });
});


describe("Avatar Gallery", function() {
  beforeEach(function() {
    misago._context = {
      MEDIA_URL: '/test-media/'
    };
  });

  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function() {
    /* jshint ignore:start */
    testUtils.render(
      <Gallery name="Test gallery"
               images={apiResponse.galleries[0].images} />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .avatars-gallery');
    assert.ok(element.length, "component renders");
    assert.equal(element.find('h3').text().trim(), "Test gallery",
      "gallery title is rendered");

    apiResponse.galleries[0].images.forEach(function(i) {
      assert.ok(element.find('button>img[src="/test-media/' + i + '"]').length,
        "component contains image");
    });
  });

  it("passess callback", function(done) { // jshint ignore:line
    /* jshint ignore:start */
    let select = function(image) {
      assert.equal(image, "avatars/Nature/arctic_fox.jpg",
        "callback was called with valid argument");
      done();
    };

    testUtils.render(
      <Gallery name="Test gallery"
               images={apiResponse.galleries[0].images}
               select={select} />
    );
    /* jshint ignore:end */

    testUtils.simulateClick("#test-mount button");
  });

  it("disables buttons", function() {
    /* jshint ignore:start */
    testUtils.render(
      <Gallery name="Test gallery"
               images={apiResponse.galleries[0].images}
               disabled={true} />
    );
    /* jshint ignore:end */

    apiResponse.galleries[0].images.forEach(function(i) {
      let image = $('#test-mount button>img[src="/test-media/' + i + '"]');
      assert.ok(image.parent().attr('disabled'), "has disabled attr");
      assert.ok(image.parent().hasClass('btn-disabled'), "has disabled class");
    });
  });
});

describe("Avatar Gallery Item", function() {
  beforeEach(function() {
    misago._context = {
      MEDIA_URL: '/test-media/'
    };
  });

  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders", function() {
    /* jshint ignore:start */
    testUtils.render(
      <GalleryItem image="avatars/Nature/arctic_fox.jpg"
                   disabled={false}
                   selection={null} />
    );
    /* jshint ignore:end */

    let element = $('#test-mount button');
    assert.ok(element.length, "component renders");
    assert.ok(!element.hasClass('avatar-selected'), "item is not selected");

    assert.equal(
      element.find('img').attr('src'),
      '/test-media/avatars/Nature/arctic_fox.jpg',
      "component builds valid image url");
  });

  it("renders selected", function() {
    /* jshint ignore:start */
    testUtils.render(
      <GalleryItem image="avatars/Nature/arctic_fox.jpg"
                   disabled={false}
                   selection="avatars/Nature/arctic_fox.jpg" />
    );
    /* jshint ignore:end */

    let element = $('#test-mount button');
    assert.ok(element.length, "component renders");
    assert.ok(element.hasClass('avatar-selected'), "item is selected");
  });

  it("renders disabled", function() {
    /* jshint ignore:start */
    testUtils.render(
      <GalleryItem image="avatars/Nature/arctic_fox.jpg"
                   disabled={true}
                   selection="avatars/Nature/arctic_fox.jpg" />
    );
    /* jshint ignore:end */

    let element = $('#test-mount button');
    assert.ok(element.length, "component renders");
    assert.ok(element.attr('disabled'), "has disabled attr");
    assert.ok(element.hasClass('btn-disabled'), "has disabled class");
    assert.ok(element.hasClass('avatar-selected'), "item is selected");
  });

  it("executes callback", function(done) { // jshint ignore:line
    /* jshint ignore:start */
    let select = function(image) {
      assert.equal(image, "avatars/Nature/arctic_fox.jpg",
        "callback was called with valid argument");
      done();
    };

    testUtils.render(
      <GalleryItem image="avatars/Nature/arctic_fox.jpg"
                   select={select} />
    );
    /* jshint ignore:end */

    testUtils.simulateClick('#test-mount button');
  });
});