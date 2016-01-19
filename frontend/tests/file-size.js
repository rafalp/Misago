import assert from 'assert';
import fileSize from 'misago/utils/file-size';

describe('File Size', function() {
  it("formats bytes size", function() {
    assert.equal(fileSize(33), "33 B",
      "bytes are formatted");

    assert.equal(fileSize(33 * 1000), "33 KB",
      "kilobytes are formatted");

    assert.equal(fileSize(33 * 1000 * 1000), "33 MB",
      "megabytes are formatted");

    assert.equal(fileSize(33 * 1000 * 1000 * 1000), "33 GB",
      "gigabytes are formatted");
  });
});