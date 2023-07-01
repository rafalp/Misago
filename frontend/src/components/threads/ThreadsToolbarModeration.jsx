import React from "react"
import ModerationControls from "./moderation/controls"

const ThreadsToolbarModeration = ({
  api,
  categoriesMap,
  categories,
  threads,
  addThreads,
  freezeThread,
  updateThread,
  deleteThread,
  selection,
  moderation,
  route,
  user,
  disabled,
}) => (
  <div className="dropdown threads-moderation">
    <button
      type="button"
      className="btn btn-default btn-outline btn-icon dropdown-toggle"
      title={pgettext("threads list nav", "Moderation")}
      data-toggle="dropdown"
      aria-haspopup="true"
      aria-expanded="false"
      disabled={disabled}
    >
      <span className="material-icon">settings</span>
    </button>
    <ModerationControls
      api={api}
      categories={categories}
      categoriesMap={categoriesMap}
      threads={threads}
      addThreads={addThreads}
      freezeThread={freezeThread}
      updateThread={updateThread}
      deleteThread={deleteThread}
      selection={selection}
      moderation={moderation}
      route={route}
      user={user}
      disabled={disabled}
    />
  </div>
)

export default ThreadsToolbarModeration
