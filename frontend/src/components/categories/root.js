import moment from 'moment';
import React from 'react';
import Category from 'misago/components/categories/category'; // jshint ignore:line
import EmptyMessage from 'misago/components/categories/empty-message'; // jshint ignore:line
import misago from 'misago/index';
import polls from 'misago/services/polls';

let dehydrate = function(category) {
  return Object.assign({}, category, {
    last_post_on: category.last_post_on ? moment(category.last_post_on) : null,
    subcategories: category.subcategories.map(dehydrate)
  });
};

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      categories: misago.get('CATEGORIES').map(dehydrate)
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
      categories: data.map(dehydrate)
    });
  };
  /* jshint ignore:end */

  getClassName() {
    if (this.state.categories.length) {
      return 'page page-categories';
    } else {
      return 'page page-categories page-message';
    }
  }

  getHeading() {
    if (misago.get('CATEGORIES_ON_INDEX')) {
      return misago.get('SETTINGS').forum_name;
    } else {
      return gettext("Categories");
    }
  }

  getCategoriesList() {
    if (this.state.categories.length) {
      /* jshint ignore:start */
      return <div className="categories-list">
        {this.state.categories.map(function(category) {
          return <Category category={category} key={category.id} />;
        })}
      </div>;
      /* jshint ignore:end */
    } else {
      /* jshint ignore:start */
      return <EmptyMessage />;
    /* jshint ignore:end */
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className={this.getClassName()}>

      <div className="page-header">
        <div className="container">
          <h1>{this.getHeading()}</h1>
        </div>
      </div>

      <div className="container">
        {this.getCategoriesList()}
      </div>

    </div>;
    /* jshint ignore:end */
  }
}

export function select(store) {
  return {
    'tick': store.tick.tick,
  };
}