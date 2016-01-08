import assert from 'assert';
import { LocalStorage } from 'misago/services/local-storage';

describe("LocalStorage", function() {
  it("changes state", function() {
    let storage = new LocalStorage();
    storage.init('test_state_change');

    assert.equal(storage.get('not-existing'), null,
      "getter returns null for nonexisting key");

    storage.set('test', {test: 'true'});
    assert.deepEqual(storage.get('test'), {test: 'true'},
      "getter returns value for existing key");

    storage.init('test_state_prefix_b');
    assert.equal(storage.get('test'), null,
      "getter returns null for different prefix");
  });
});
