import assert from 'assert';
import React from 'react'; // jshint ignore:line
import CategoryPicker from 'misago/components/threads/category-picker'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

/* jshint ignore:start */
let list = {
  name: "All",
  nameLong: "All threads",
  path: ''
};
let categories = {
  1: {
    id: 1,
    name: "First Category",
    absolute_url: '/category-1/'
  },
  3: {
    id: 3,
    name: "Second Category",
    absolute_url: '/category-3/'
  }
};
/* jshint ignore:end */

describe("Threads List Category Picker", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it("renders with invalid categories", function() {
    /* jshint ignore:start */
    testUtils.render(
      <CategoryPicker list={list}
                      categories={{}}
                      choices={[1, 3, 5]} />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .category-picker');
    assert.ok(element.length, "component renders");
    assert.ok(!element.find('li').length, "picker renders without choices");
  });

  it("renders with some invalid categories", function() {
    /* jshint ignore:start */
    testUtils.render(
      <CategoryPicker list={list}
                      categories={categories}
                      choices={[1, 2, 3, 4, 5]} />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .category-picker');
    assert.ok(element.length, "component renders");
    assert.equal(element.find('li').length, 2,
      "picker renders with only two choices");

    assert.equal(element.find('li').first().text(),
      "First Category",
      "first category is rendered in picker");
    assert.equal(element.find('li').last().text(),
      "Second Category",
      "second category is rendered in picker");
  });

  it("renders with categories", function() {
    /* jshint ignore:start */
    testUtils.render(
      <CategoryPicker list={list}
                      categories={categories}
                      choices={[1, 3]} />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .category-picker');
    assert.ok(element.length, "component renders");
    assert.equal(element.find('li').length, 2,
      "picker renders with two valid choices");

    assert.equal(element.find('li').first().text(),
      "First Category",
      "first category is rendered in picker");
    assert.equal(element.find('li').last(1).text(),
      "Second Category",
      "second category is rendered in picker");
  });
});
