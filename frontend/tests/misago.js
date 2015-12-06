import assert from 'assert';
import { Misago } from 'misago/index';

var misago = null;

describe('Misago', function() {
  it("addInitializer registers new initializer", function() {
    misago = new Misago();

    misago.addInitializer({
      name: 'test',
      init: null
    });

    assert.equal(misago._initializers[0].key, 'test',
      "test initializer was registered");

    assert.equal(misago._initializers.length, 1,
      "addInitializer() registered single initializer in container");
    assert.equal(misago._initializers[0].key, 'test',
      "addInitializer() registered test initializer in container");
  });

  it("init() calls test initializer", function() {
    misago = new Misago();

    misago.addInitializer({
      name: 'test',
      init: function(options) {
        assert.equal(options, 'tru', "initializer was called with options");
      }
    });

    misago.init('tru');
  });

  it("init() calls test initializers in order", function() {
    misago = new Misago();

    misago.addInitializer({
      name: 'carrot',
      init: function(options) {
        assert.equal(options.next, 'carrot',
          "first initializer was called in right order");

        options.next = 'apple';
      },
      before: 'apple'
    });

    misago.addInitializer({
      name: 'apple',
      init: function(options) {
        assert.equal(options.next, 'apple',
          "second initializer was called in right order");

        options.next = 'orange';
      }
    });

    misago.addInitializer({
      name: 'orange',
      init: function(options) {
        assert.equal(options.next, 'orange',
          "pen-ultimate initializer was called in right order");

        options.next = 'banana';
      },
      before: '_end'
    });

    misago.addInitializer({
      name: 'banana',
      init: function(options) {
        assert.equal(options.next, 'banana',
          "ultimate initializer was called in right order");
      },
      after: 'orange'
    });

    misago.init({next: 'carrot'});
  });
});
