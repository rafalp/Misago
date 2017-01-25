import React from 'react'; // jshint ignore:line
import CategoryPicker from 'misago/components/threads/category-picker'; // jshint ignore:line
import ModerationControls from 'misago/components/threads/moderation/controls'; // jshint ignore:line
import SelectionControls from 'misago/components/threads/moderation/selection'; // jshint ignore:line

export default class extends React.Component {
  getCategoryPicker() {
    if (this.props.subcategories.length) {
      /* jshint ignore:start */
      return <div className="toolbar-left">
        <CategoryPicker choices={this.props.subcategories}
                        categories={this.props.categoriesMap}
                        list={this.props.list} />
      </div>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  showModerationOptions() {
    return this.props.user.id && this.props.moderation.allow;
  }

  getSelectionButton() {
    if (this.showModerationOptions()) {
      /* jshint ignore:start */
      return <div className="toolbar-right dropdown">
        <button type="button"
                className="btn btn-default btn-icon dropdown-toggle"
                data-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false"
                disabled={this.props.disabled}>
          <span className="material-icon">
            select_all
          </span>
        </button>

        <SelectionControls className="dropdown-menu dropdown-menu-right"
                           threads={this.props.threads} />

      </div>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getSelectedThreads() {
    return this.props.threads.filter((thread) => {
      return this.props.selection.indexOf(thread.id) >= 0;
    });
  }

  getModerationButton() {
    if (this.showModerationOptions()) {
      /* jshint ignore:start */
      return <div className="toolbar-right dropdown">
        <button type="button"
                className="btn btn-default dropdown-toggle"
                data-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false"
                disabled={this.props.disabled || !this.props.selection.length}>
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

      </div>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className="toolbar with-js">
      {this.getCategoryPicker()}
      {this.getSelectionButton()}
      {this.getModerationButton()}
    </div>;
    /* jshint ignore:end */
  }
}