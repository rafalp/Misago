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
                        categories={this.props.categories}
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
            check_box_outline_blank
          </span>
        </button>

        <SelectionControls className="dropdown-menu dropdown-menu-right"
                           selectAll={this.props.selectAllThreads}
                           selectNone={this.props.selectNoneThreads} />

      </div>;
      /* jshint ignore:end */
    } else {
      return null;
    }
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
          {gettext("Moderation")}
        </button>

        <ModerationControls className="dropdown-menu dropdown-menu-right"
                            moderation={this.props.moderation}
                            threads={this.props.selection}
                            freezeThread={this.props.freezeThread}
                            updateThread={this.props.updateThread} />

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
      <p className="toolbar-left hidden-xs hidden-sm">
        {this.props.children}
      </p>
      {this.getSelectionButton()}
      {this.getModerationButton()}
    </div>;
    /* jshint ignore:end */
  }
}