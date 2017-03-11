import React from 'react'; // jshint ignore:line
import CategoryPicker from 'misago/components/threads/category-picker'; // jshint ignore:line
import ModerationControls from 'misago/components/threads/moderation/controls'; // jshint ignore:line
import SelectionControls from 'misago/components/threads/moderation/selection'; // jshint ignore:line

export default class extends React.Component {
  getCategoryPicker() {
    if (!this.props.subcategories.length) return null;

    /* jshint ignore:start */
    return (
      <div className="col-xs-3 col-sm-3 col-md-2 dropdown">
        <CategoryPicker
          categories={this.props.categoriesMap}
          choices={this.props.subcategories}
          list={this.props.list}
        />
      </div>
    );
    /* jshint ignore:end */
  }

  showModerationOptions() {
    return this.props.user.id && this.props.moderation.allow;
  }

  getSelectedThreads() {
    return this.props.threads.filter((thread) => {
      return this.props.selection.indexOf(thread.id) >= 0;
    });
  }

  getModerationButton() {
    if (!this.showModerationOptions()) return null;

    /* jshint ignore:start */
    return (
      <div className="col-xs-6 col-sm-3 col-md-2 dropdown">
        <button
          type="button"
          className="btn btn-default dropdown-toggle btn-block"
          data-toggle="dropdown"
          aria-haspopup="true"
          aria-expanded="false"
          disabled={this.props.disabled || !this.props.selection.length}
        >
          <span className="material-icon">
            settings
          </span>
          {gettext("Options")}
        </button>

        <ModerationControls
          addThreads={this.props.addThreads}
          categories={this.props.categories}
          categoriesMap={this.props.categoriesMap}
          className="dropdown-menu dropdown-menu-right"
          deleteThread={this.props.deleteThread}
          freezeThread={this.props.freezeThread}
          moderation={this.props.moderation}
          route={this.props.route}
          threads={this.getSelectedThreads()}
          updateThread={this.props.updateThread}
          user={this.props.user}
        />

      </div>
    );
    /* jshint ignore:end */
  }

  getSelectionButton() {
    if (!this.showModerationOptions()) return null;

    /* jshint ignore:start */
    return (
      <div className="col-xs-3 col-sm-2 col-md-1 dropdown">
        <button
          type="button"
          className="btn btn-default btn-icon dropdown-toggle btn-block"
          data-toggle="dropdown"
          aria-haspopup="true"
          aria-expanded="false"
          disabled={this.props.disabled}
        >
          <span className="material-icon">
            select_all
          </span>
        </button>

        <SelectionControls
          className="dropdown-menu dropdown-menu-right"
          threads={this.props.threads}
        />
      </div>
    );
    /* jshint ignore:end */
  }

  render() {
    /* jshint ignore:start */
    return (
      <div className="row row-toolbar row-toolbar-bottom-margin">
        {this.getCategoryPicker()}
        <div className="hidden-xs col-sm-4 col-md-7" />
        {this.getModerationButton()}
        {this.getSelectionButton()}
      </div>
    );
    /* jshint ignore:end */
  }
}