import assert from 'assert';
import stringCount from 'misago/utils/string-count';

describe('String Count', function() {
  it("counts number of occurences of needle in haystack", function() {
    assert.equal(stringCount("lorem ipsum", "dolor"), 0,
      "nonexistant needle wasn't found in haystack");

    assert.equal(stringCount("lorem ipsum", "ore"), 1,
      "needle was found in haystack once");

    assert.equal(stringCount("lOrEm ipsum", "oRe"), 1,
      "search is case-insensitive");

    assert.equal(stringCount("lorem ipsum dolorem met.", "ore"), 2,
      "needle was found in haystack twice");
  });
});