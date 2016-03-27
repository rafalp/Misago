import assert from 'assert';
import escapeHtml from 'misago/utils/escape-html';

describe('Escape HTML', function() {
  it("escapes html", function() {
    assert.equal(escapeHtml("lorem ipsum"), "lorem ipsum",
      "no unsafe characters were handled");

    assert.equal(escapeHtml("lorem <b>ipsum</b>"),
      "lorem &lt;b&gt;ipsum&lt;/b&gt;",
      "html tags were escaped");

    assert.equal(escapeHtml("lorem \"ipsum\""), "lorem &quot;ipsum&quot;",
      "quotes were escaped");

    assert.equal(escapeHtml("lorem 'ipsum'"), "lorem &#039;ipsum&#039;",
      "single quotes were escaped");
  });
});