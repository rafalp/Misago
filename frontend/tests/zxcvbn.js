import assert from 'assert';
import { Zxcvbn } from 'misago/services/zxcvbn';

let zxcvbn = null;

describe("Zxcvbn", function() {
  afterEach(function() {
    delete window.zxcvbn;
  });

  it("loads library", function(done) {
    zxcvbn = new Zxcvbn();
    zxcvbn.init({
      include: function(lib) {
        assert.equal(lib, "misago/js/zxcvbn.js", "library is requested");
      }
    });

    zxcvbn.load().then(function() {
      assert.ok(true, "zxcvbn lib was loaded");
      done();
    });

    window.setTimeout(function() {
      window.zxcvbn = true;
    }, 200);
  });

  it("scores passwords", function(done) {
    zxcvbn = new Zxcvbn();
    zxcvbn.init({
      include: function(lib) {
        assert.equal(lib, 'misago/js/zxcvbn.js', "library is requested");
      }
    });

    zxcvbn.load().then(function() {
      assert.equal(zxcvbn.scorePassword('abcd'), 4, "returns pass score");
      done();
    });

    window.setTimeout(function() {
      window.zxcvbn = function(password) {
        assert.equal(password, 'abcd', "calls underlying zxcvbn lib");
        return {score: password.length};
      };
    }, 200);
  });
});