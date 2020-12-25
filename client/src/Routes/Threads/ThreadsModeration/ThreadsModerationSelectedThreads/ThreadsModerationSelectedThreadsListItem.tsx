import classnames from "classnames"
import React from "react"
import { Checkbox } from "../../../../UI/Checkbox"
import { TidbitCategory, TidbitReplies, Tidbits } from "../../../../UI/Tidbits"
import { ThreadValidationError } from "../../../../UI/ValidationError"
import { MutationError } from "../../../../types"
import { ISelectedThread } from "../../Threads.types"

interface ThreadsModerationSelectedThreadsListItemProps {
  disabled?: boolean
  error?: MutationError
  id?: string
  selected?: boolean
  thread: ISelectedThread
  changeSelection: (id: string, selected: boolean) => void
}

const ThreadsModerationSelectedThreadsListItem: React.FC<ThreadsModerationSelectedThreadsListItemProps> = ({
  disabled,
  error,
  id,
  selected,
  thread,
  changeSelection,
}) => {
  const itemId = id ? id + "_" + thread.id : undefined

  return (
    <li
      className={classnames("selected-item selected-thread", {
        "is-invalid": !!error,
      })}
    >
      {error && (
        <ThreadValidationError error={error}>
          {({ message }) => (
            <div className="selected-item-error">{message}</div>
          )}
        </ThreadValidationError>
      )}
      <div className="row row-nogutters">
        <div className="col selected-item-body">
          <label className="selected-thread-title" htmlFor={itemId}>
            {thread.title}
          </label>
          <div className="selected-thread-tidbits">
            <Tidbits>
              {thread.category.parent && (
                <TidbitCategory
                  category={thread.category.parent}
                  disabled
                  parent
                />
              )}
              <TidbitCategory category={thread.category} disabled />
              {thread.replies > 0 && <TidbitReplies value={thread.replies} />}
            </Tidbits>
          </div>
        </div>
        <div className="col-auto selected-item-checkbox">
          <Checkbox
            checked={selected}
            disabled={disabled}
            id={itemId}
            onChange={(event) => {
              changeSelection(thread.id, event.target.checked)
            }}
          />
        </div>
      </div>
    </li>
  )
}

export default ThreadsModerationSelectedThreadsListItem
