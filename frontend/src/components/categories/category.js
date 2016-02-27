import React from 'react';
import LastActivity from 'misago/components/categories/last-activity'; // jshint ignore:line
import ReadIcon from 'misago/components/categories/read-icon'; // jshint ignore:line
import Stats from 'misago/components/categories/stats'; // jshint ignore:line

export default class extends React.Component {
  getClassName() {
    if (this.props.category.css_class) {
      return 'panel panel-default panel-category panel-category-' + this.props.category.css_class;
    } else {
      return 'panel panel-default panel-category';
    }
  }

  getHeadingClassName() {
    if (this.props.category.subcategories.length) {
      return 'panel-heading';
    } else {
      return 'panel-heading heading-alone';
    }
  }

  getCategoryDescription() {
    if (this.props.category.description) {
      /* jshint ignore:start */
      return <div className="panel-body category-description"
                  dangerouslySetInnerHTML={{
                    __html: this.props.category.description.html
                  }} />;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getSubcategoryClass(category) {
    if (category.css_class) {
      return 'list-group-item category-subcategory subcategory-' + category.css_class;
    } else {
      return 'list-group-item category-subcategory';
    }
  }

  getSubcategoryDescription(category) {
    if (category.description) {
      /* jshint ignore:start */
      return <div className="subcategory-description"
                  dangerouslySetInnerHTML={{
                    __html: category.description.html
                  }} />;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getSubcategorySubcategoryClass(category) {
    if (category.css_class) {
      return 'subcategory subcategory-' + category.css_class;
    } else {
      return 'subcategory';
    }
  }

  getSubcategorySubcategories(category) {
    if (category.subcategories.length) {
      /* jshint ignore:start */
      return <ul className="list-inline subcategory-subcategories">
        {category.subcategories.map((category) => {
          return <li key={category.id}>
            <a href={category.absolute_url}
               className={this.getSubcategorySubcategoryClass(category)}>
              {category.name}
            </a>
          </li>;
        })}
      </ul>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getSubcategories() {
    if (this.props.category.subcategories.length) {
      /* jshint ignore:start */
      return <ul className="list-group category-subcategories">
        {this.props.category.subcategories.map((category) => {
          return <li className={this.getSubcategoryClass(category)}
                     key={category.id}>
            <div className="title-row">
              <h4>
                <ReadIcon category={category} />
                <a href={category.absolute_url} className="item-title">
                  {category.name}
                </a>
              </h4>
              <Stats category={category} />
            </div>

            <LastActivity category={category} />

            {this.getSubcategoryDescription(category)}
            {this.getSubcategorySubcategories(category)}

          </li>;
        })}
      </ul>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    return <div id={'panel-category-' + this.props.category.id}
                className={this.getClassName()}>
      <div className={this.getHeadingClassName()}>
        <div className="panel-heading-inblock">
          <div className="panel-heading-top-row">
            <h3 className="panel-title">
              <ReadIcon category={this.props.category} />
              <a href={this.props.category.absolute_url} className="item-title">
                {this.props.category.name}
              </a>
            </h3>
            <Stats category={this.props.category} />
          </div>
          <LastActivity category={this.props.category} />
        </div>
      </div>

      {this.getCategoryDescription()}

      {this.getSubcategories()}

    </div>;
    /* jshint ignore:end */
  }
}