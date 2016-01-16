import assert from 'assert';
import { Cropit } from 'misago/services/cropit';

let cropit = null;

describe("Cropit", function() {
  afterEach(function() {
    delete window.$.cropit;
  });

  it("loads library", function(done) {
    cropit = new Cropit();
    cropit.init({
      include: function(lib) {
        assert.equal(lib, "misago/js/jquery.cropit.js", "library is requested");
      }
    });

    cropit.load().then(function() {
      assert.ok(true, "cropit lib was loaded");
      done();
    });

    window.setTimeout(function() {
      window.$.cropit = true;
    }, 200);
  });
});