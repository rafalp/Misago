import assert from 'assert';
import React from 'react'; // jshint ignore:line
import PageLead from 'misago/components/page-lead'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

describe("Page Lead", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it('renders with lead class', function() {
    /* jshint ignore:start */
    testUtils.render(<PageLead copy='<p>Lorem ipsum dolor.</p>' />);
    /* jshint ignore:end */

    let element = $('#test-mount .page-lead.lead');
    assert.ok(element.length, "component renders");
    assert.equal(element.find('p').text(), 'Lorem ipsum dolor.',
      "component displays given html");
  });

  it('renders without lead class', function() {
    /* jshint ignore:start */
    testUtils.render(<PageLead copy='<p>Lorem ipsum.</p><p>Dolor.</p>' />);
    /* jshint ignore:end */

    let element = $('#test-mount .page-lead');
    assert.ok(element.length, "component renders");
    assert.ok(!element.hasClass('lead'), "lead class is hidden");
  });
});
