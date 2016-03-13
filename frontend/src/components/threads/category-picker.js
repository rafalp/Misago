import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line

export class Subcategory extends React.Component {
  getUrl() {
    if (this.props.listPath) {
      return this.props.category.absolute_url + this.props.listPath;
    } else {
      return this.props.category.absolute_url;
    }
  }

  getClassName() {
    if (this.props.category.css_class) {
      return 'subcategory subcategory-' + this.props.category.css_class;
    } else {
      return 'subcategory';
    }
  }

  render() {
    /* jshint ignore:start */
    return <li>
      <Link to={this.getUrl()} className={this.getClassName()}>
        {this.props.category.name}
      </Link>
    </li>;
    /* jshint ignore:end */
  }
}

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return <ul className="list-inline subcategories-list">
      {this.props.choices.map((id) => {
        if (this.props.categories[id]) {
          return <Subcategory category={this.props.categories[id]}
                              listPath={this.props.list.path}
                              key={id} />;
        } else {
          return null;
        }
      })}
    </ul>;
    /* jshint ignore:end */
  }
}