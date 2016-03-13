import React from 'react';
import CategorySubcategories from 'misago/components/categories/category-subcategories'; // jshint ignore:line
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

  getSubcategories() {
    if (this.props.category.subcategories.length) {
      /* jshint ignore:start */
      return <CategorySubcategories categories={this.props.category.subcategories} />;
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