import React from 'react';
import PageLead from 'misago/components/page-lead'; // jshint ignore:line
import Toolbar from 'misago/components/threads/toolbar'; // jshint ignore:line

export default class extends React.Component {
  getCategoryDescription() {
    if (this.props.pageLead) {
      /* jshint ignore:start */
      return (
        <div className="category-description">
          <div className="page-lead">
            <p>{this.props.pageLead}</p>
          </div>
        </div>
      );
      /* jshint ignore:end */
    } else if (this.props.route.category.description) {
      /* jshint ignore:start */
      return (
        <div className="category-description">
          <PageLead copy={this.props.route.category.description.html} />
        </div>
      );
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getDisableToolbar() {
    return !this.props.isLoaded || this.props.isBusy || this.props.busyThreads.length;
  }

  getToolbar() {
    if (this.props.subcategories.length || this.props.user.id) {
      /* jshint ignore:start */
      return <Toolbar subcategories={this.props.subcategories}
                      categories={this.props.route.categories}
                      categoriesMap={this.props.route.categoriesMap}
                      list={this.props.route.list}

                      threads={this.props.threads}
                      moderation={this.props.moderation}
                      selection={this.props.selection}
                      selectAllThreads={this.props.selectAllThreads}
                      selectNoneThreads={this.props.selectNoneThreads}

                      addThreads={this.props.addThreads}
                      freezeThread={this.props.freezeThread}
                      deleteThread={this.props.deleteThread}
                      updateThread={this.props.updateThread}

                      route={this.props.route}
                      disabled={this.getDisableToolbar()}
                      user={this.props.user}>
      </Toolbar>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className="container">

      {this.getCategoryDescription()}
      {this.getToolbar()}

      {this.props.children}

    </div>;
    /* jshint ignore:end */
  }
}