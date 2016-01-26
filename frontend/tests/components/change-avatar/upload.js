import assert from 'assert';
import React from 'react'; // jshint ignore:line
import UploadAvatar from 'misago/components/change-avatar/upload'; // jshint ignore:line
import misago from 'misago/index';
import * as testUtils from 'misago/utils/test-utils';

let component = null;

/* jshint ignore:start */
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
/* jshint ignore:end */

describe("Upload Avatar", function() {
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
  });

  it("renders", function(done) {
    /* jshint ignore:start */
    testUtils.render(
      <UploadAvatar options={apiResponse} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .modal-avatar-upload', function() {
      let element = $('#test-mount .modal-avatar-upload');
      assert.ok(true, "component renders");

      assert.equal(element.find('p').text().trim(),
        "gif, png, jpg, jpeg files smaller than 750 KB",
        "valid help text is displayed");

      done();
    });
  });

  it("validates image", function(done) {
    /* jshint ignore:start */
    component = testUtils.render(
      <UploadAvatar options={apiResponse} />
    );
    /* jshint ignore:end */

    testUtils.onElement('#test-mount .modal-avatar-upload', function() {
      assert.equal(component.validateFile({'size': 83 * 100 * 1000}),
        "Selected file is too big. (8.3 MB)",
        "too large file is rejected");

      assert.equal(component.validateFile(
        {'size': 83 * 1000, 'type': "image/bmp"}),
        "Selected file type is not supported.",
        "invalid file mime type is rejected");

      assert.equal(component.validateFile(
        {'size': 83 * 1000, 'type': "image/png", 'name': 'test.bmp'}),
        "Selected file type is not supported.",
        "invalid file extension is rejected");

      assert.equal(component.validateFile(
        {'size': 83 * 1000, 'type': "image/png", 'name': 'test.png'}), false,
        "file raises no errors");

      done();
    });
  });
});