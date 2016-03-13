import moment from 'moment';
import React from 'react';
import Category from 'misago/components/categories/category'; // jshint ignore:line
import misago from 'misago/index';
import polls from 'misago/services/polls';

let hydrate = function(category) {
  return Object.assign({}, category, {
    last_post_on: category.last_post_on ? moment(category.last_post_on) : null,
    subcategories: category.subcategories.map(hydrate)
  });
};

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      categories: misago.get('CATEGORIES').map(hydrate)
    };

    this.startPolling(misago.get('CATEGORIES_API'));
  }

  startPolling(api) {
    polls.start({
      poll: 'categories',
      url: api,
      frequency: 180 * 1000,
      update: this.update
    });
  }

  /* jshint ignore:start */
  update = (data) => {
    this.setState({
      categories: data.map(hydrate)
    });
  };
  /* jshint ignore:end */

  render() {
    /* jshint ignore:start */
    return <div className="categories-list">
      {this.state.categories.map(function(category) {
        return <Category category={category} key={category.id} />;
      })}
    </div>;
    /* jshint ignore:end */
  }
}

export function select(store) {
  return {
    'tick': store.tick.tick,
  };
}