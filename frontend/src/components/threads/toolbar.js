import React from 'react'; // jshint ignore:line
import CategoryPicker from 'misago/components/threads/category-picker'; // jshint ignore:line
import ModerationMenu from 'misago/components/threads/moderation/menu'; // jshint ignore:line

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

  getModerationButton() {
    if (this.props.user.id && this.props.moderation.allow) {
      /* jshint ignore:start */
      let selectedThreads = this.props.threads.filter((thread) => {
        return this.props.selection.indexOf(thread.id) >= 0;
      });

      return <div className="dropdown toolbar-right">
        <button type="button"
                className="btn btn-default dropdown-toggle"
                data-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false"
                disabled={!this.props.isLoaded || !selectedThreads.length}>
          <span className="material-icon">
            settings
          </span>
          {gettext("Moderation")}
        </button>
        <ModerationMenu className="dropdown-menu dropdown-menu-right"
                        threads={selectedThreads}
                        moderation={this.props.moderation}
                        selection={this.props.selection}

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
      {this.getModerationButton()}
    </div>;
    /* jshint ignore:end */
  }
}