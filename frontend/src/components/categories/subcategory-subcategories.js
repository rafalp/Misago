import React from 'react';
import SubcategorySubcategories from 'misago/components/categories/subcategory-subcategories'; // jshint ignore:line

export default class Subcategory extends React.Component {
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
      <a href={this.props.category.absolute_url}
         className={this.getClassName()}>
        {this.props.category.name}
      </a>
    </li>;
    /* jshint ignore:end */
  }
}

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return <ul className="list-inline subcategories-list">
      {this.props.categories.map((category) => {
        return <Subcategory category={category} key={category.id} />;
      })}
    </ul>;
    /* jshint ignore:end */
  }
}