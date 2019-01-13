import React from "react"
import Form from "misago/components/form"
import FormGroup from "misago/components/form-group"
import CategorySelect from "misago/components/category-select"
import * as select from "misago/reducers/selection"
import { filterThreads } from "misago/reducers/threads"
import modal from "misago/services/modal"
import store from "misago/services/store"

export default class extends Form {
  constructor(props) {
    super(props)

    this.state = {
      category: null
    }

    const acls = {}
    for (const i in props.user.acl.categories) {
      if (!props.user.acl.categories.hasOwnProperty(i)) {
        continue
      }

      const acl = props.user.acl.categories[i]
      acls[acl.id] = acl
    }

    this.categoryChoices = []
    props.categories.forEach(category => {
      if (category.level > 0) {
        const acl = acls[category.id]
        const disabled =
          !acl.can_start_threads ||
          (category.is_closed && !acl.can_close_threads)

        this.categoryChoices.push({
          value: category.id,
          disabled: disabled,
          level: category.level - 1,
          label: category.name
        })

        if (!disabled && !this.state.category) {
          this.state.category = category.id
        }
      }
    })
  }

  handleSubmit = event => {
    // we don't reload page on submissions
    event.preventDefault()

    modal.hide()

    const onSuccess = () => {
      store.dispatch(
        filterThreads(this.props.route.category, this.props.categoriesMap)
      )

      // deselect threads moved outside of visible scope
      const storeState = store.getState()
      const leftThreads = storeState.threads.map(thread => thread.id)
      store.dispatch(
        select.all(
          storeState.selection.filter(thread => {
            return leftThreads.indexOf(thread) !== -1
          })
        )
      )
    }

    this.props.callApi(
      [
        { op: "replace", path: "category", value: this.state.category },
        { op: "replace", path: "flatten-categories", value: null },
        { op: "add", path: "acl", value: true }
      ],
      gettext("Selected threads were moved."),
      onSuccess
    )
  }

  getClassName() {
    if (!this.state.category) {
      return "modal-dialog modal-message"
    } else {
      return "modal-dialog"
    }
  }

  renderForm() {
    return (
      <form onSubmit={this.handleSubmit}>
        <div className="modal-body">
          <FormGroup label={gettext("New category")} for="id_new_category">
            <CategorySelect
              id="id_new_category"
              onChange={this.bindInput("category")}
              value={this.state.category}
              choices={this.categoryChoices}
            />
          </FormGroup>
        </div>
        <div className="modal-footer">
          <button
            className="btn btn-default"
            data-dismiss="modal"
            disabled={this.state.isLoading}
            type="button"
          >
            {gettext("Cancel")}
          </button>
          <button className="btn btn-primary">{gettext("Move threads")}</button>
        </div>
      </form>
    )
  }

  renderCantMoveMessage() {
    return (
      <div className="modal-body">
        <div className="message-icon">
          <span className="material-icon">info_outline</span>
        </div>
        <div className="message-body">
          <p className="lead">
            {gettext(
              "You can't move threads because there are no categories you are allowed to move them to."
            )}
          </p>
          <p>
            {gettext(
              "You need permission to start threads in category to be able to move threads to it."
            )}
          </p>
          <button
            className="btn btn-default"
            data-dismiss="modal"
            type="button"
          >
            {gettext("Ok")}
          </button>
        </div>
      </div>
    )
  }

  render() {
    return (
      <div className={this.getClassName()} role="document">
        <div className="modal-content">
          <div className="modal-header">
            <button
              type="button"
              className="close"
              data-dismiss="modal"
              aria-label={gettext("Close")}
            >
              <span aria-hidden="true">&times;</span>
            </button>
            <h4 className="modal-title">{gettext("Move threads")}</h4>
          </div>
          {this.state.category
            ? this.renderForm()
            : this.renderCantMoveMessage()}
        </div>
      </div>
    )
  }
}
