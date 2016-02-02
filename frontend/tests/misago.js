import assert from 'assert';
import { Misago } from 'misago/index';

var misago = null;

describe('Misago', function() {
  it("addInitializer registers new initializer", function() {
    misago = new Misago();

    misago.addInitializer({
      name: 'test',
      initializer: null
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
      initializer: function(misago) {
        assert.equal(misago, misago, "initializer was called with context");
        assert.equal(misago._context, 'tru', "context is preserved");
      }
    });

    misago.init('tru');
  });

  it("init() calls test initializers in order", function() {
    misago = new Misago();

    misago.addInitializer({
      name: 'carrot',
      initializer: function(misago) {
        assert.equal(misago._context.next, 'carrot',
          "first initializer was called in right order");

        misago._context.next = 'apple';
      },
      before: 'apple'
    });

    misago.addInitializer({
      name: 'apple',
      initializer: function(misago) {
        assert.equal(misago._context.next, 'apple',
          "second initializer was called in right order");

        misago._context.next = 'orange';
      }
    });

    misago.addInitializer({
      name: 'orange',
      initializer: function(misago) {
        assert.equal(misago._context.next, 'orange',
          "pen-ultimate initializer was called in right order");

        misago._context.next = 'banana';
      },
      before: '_end'
    });

    misago.addInitializer({
      name: 'banana',
      initializer: function(misago) {
        assert.equal(misago._context.next, 'banana',
          "ultimate initializer was called in right order");
      },
      after: 'orange'
    });

    misago.init({next: 'carrot'});
  });

  it("has() tests if context has value", function() {
    misago = new Misago();
    misago.init({valid: 'okay'});

    assert.equal(misago.has('invalid'), false,
      "has() returned false for nonexisting key");
    assert.equal(misago.has('valid'), true,
      "has() returned true for existing key");
  });

  it("get() allows access to context values", function() {
    misago = new Misago();
    misago.init({valid: 'okay'});

    assert.equal(misago.get('invalid'), undefined,
      "get() returned undefined for nonexisting key");
    assert.equal(misago.get('invalid', 'fallback'), 'fallback',
      "get() returned fallback value for nonexisting key");
    assert.equal(misago.get('valid'), 'okay',
      "get() returned value for existing key");
    assert.equal(misago.get('valid', 'fallback'), 'okay',
      "get() returned value for existing key instead of fallback");
  });

  it("pop() allows single time access to context values", function() {
    misago = new Misago();
    misago.init({valid: 'okay'});

    assert.equal(misago.pop('invalid'), undefined,
      "pop() returned undefined for nonexisting key");
    assert.equal(misago.pop('valid'), 'okay',
      "pop() returned value for existing key");
    assert.equal(misago.get('valid'), null,
      "get() returned null for popped value");
  });
});
