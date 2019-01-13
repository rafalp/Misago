import React from "react"
import CategoryPicker from "misago/components/threads/category-picker"
import ModerationControls from "misago/components/threads/moderation/controls"
import SelectionControls from "misago/components/threads/moderation/selection"

export default class extends React.Component {
  getCategoryPicker() {
    if (!this.props.subcategories.length) return null

    return (
      <CategoryPicker
        categories={this.props.categoriesMap}
        choices={this.props.subcategories}
        list={this.props.list}
      />
    )
  }

  showModerationOptions() {
    return this.props.user.id && this.props.moderation.allow
  }

  getSelectedThreads() {
    return this.props.threads.filter(thread => {
      return this.props.selection.indexOf(thread.id) >= 0
    })
  }

  getModerationButton() {
    if (!this.showModerationOptions()) return null

    return (
      <div className="col-xs-6 col-sm-3 col-md-2">
        <div className="btn-group btn-group-justified">
          <div className="btn-group dropdown">
            <button
              type="button"
              className="btn btn-default btn-outline dropdown-toggle"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
              disabled={this.props.disabled || !this.props.selection.length}
            >
              <span className="material-icon">settings</span>
              {gettext("Options")}
            </button>

            <ModerationControls
              addThreads={this.props.addThreads}
              api={this.props.api}
              categories={this.props.categories}
              categoriesMap={this.props.categoriesMap}
              className="dropdown-menu dropdown-menu-right stick-to-bottom"
              deleteThread={this.props.deleteThread}
              freezeThread={this.props.freezeThread}
              moderation={this.props.moderation}
              route={this.props.route}
              threads={this.getSelectedThreads()}
              updateThread={this.props.updateThread}
              user={this.props.user}
            />
          </div>
        </div>
      </div>
    )
  }

  getSelectionButton() {
    if (!this.showModerationOptions()) return null

    return (
      <div className="col-xs-3 col-sm-2 col-md-1">
        <div className="btn-group btn-group-justified">
          <div className="btn-group dropdown">
            <button
              type="button"
              className="btn btn-default btn-outline btn-icon dropdown-toggle"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
              disabled={this.props.disabled}
            >
              <span className="material-icon">select_all</span>
            </button>

            <SelectionControls
              className="dropdown-menu dropdown-menu-right stick-to-bottom"
              threads={this.props.threads}
            />
          </div>
        </div>
      </div>
    )
  }

  render() {
    return (
      <div className="row row-toolbar row-toolbar-bottom-margin">
        <div className="col-xs-3 col-sm-3 col-md-2 dropdown">
          {this.getCategoryPicker()}
        </div>
        <div className="hidden-xs col-sm-4 col-md-7" />
        {this.getModerationButton()}
        {this.getSelectionButton()}
      </div>
    )
  }
}
