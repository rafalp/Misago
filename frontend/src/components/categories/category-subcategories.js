import React from 'react';
import LastActivity from 'misago/components/categories/last-activity'; // jshint ignore:line
import ReadIcon from 'misago/components/categories/read-icon'; // jshint ignore:line
import Stats from 'misago/components/categories/stats'; // jshint ignore:line
import SubcategorySubcategories from 'misago/components/categories/subcategory-subcategories'; // jshint ignore:line

export default class Subcategory extends React.Component {
  getClassName() {
    if (this.props.category.css_class) {
      return 'list-group-item category-subcategory subcategory-' + this.props.category.css_class;
    } else {
      return 'list-group-item category-subcategory';
    }
  }

  getDescription() {
    if (this.props.category.description) {
      /* jshint ignore:start */
      return <div className="subcategory-description"
                  dangerouslySetInnerHTML={{
                    __html: this.props.category.description.html
                  }} />;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getSubcategories() {
    if (this.props.category.subcategories.length) {
      /* jshint ignore:start */
      return <SubcategorySubcategories categories={this.props.category.subcategories} />;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    return <li className={this.getClassName()}>
      <div className="title-row">
        <h4>
          <ReadIcon category={this.props.category} />
          <a href={this.props.category.absolute_url} className="item-title">
            {this.props.category.name}
          </a>
        </h4>
        <Stats category={this.props.category} />
      </div>

      <LastActivity category={this.props.category} />

      {this.getDescription()}
      {this.getSubcategories()}

    </li>;
    /* jshint ignore:end */
  }
}

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return <ul className="list-group category-subcategories">
      {this.props.categories.map((category) => {
        return <Subcategory category={category} key={category.id} />;
      })}
    </ul>;
    /* jshint ignore:end */
  }
}