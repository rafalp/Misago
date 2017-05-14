// jshint ignore:start
import moment from 'moment';
import React from 'react';
import Blankslate from './blankslate';
import CategoriesList from './categories-list';
import misago from 'misago/index';
import polls from 'misago/services/polls';

const hydrate = function(category) {
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

  update = (data) => {
    this.setState({
      categories: data.map(hydrate)
    });
  };

  render() {
    const { categories } = this.state;

    if (categories.length === 0) {
      return (
        <Blankslate />
      );
    }

    return (
      <CategoriesList categories={categories} />
    );
  }
}

export function select(store) {
  return {
    'tick': store.tick.tick,
  };
}