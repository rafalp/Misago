import classNames from "classnames"
import React from "react"
import {
  Checkbox,
  FieldError,
  ThreadValidationError,
  TidbitCategory,
  TidbitReplies,
  Tidbits,
} from "../../../../UI"
import { IMutationError } from "../../../../types"
import { ISelectedThread } from "../../Threads.types"

interface IThreadsModerationSelectedThreadsListItemProps {
  disabled?: boolean
  error?: IMutationError
  id?: string
  selected?: boolean
  thread: ISelectedThread
  changeSelection: (id: string, selected: boolean) => void
}

const ThreadsModerationSelectedThreadsListItem: React.FC<IThreadsModerationSelectedThreadsListItemProps> = ({
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
      className={classNames("selected-threads-thread", {
        "is-invalid": !!error,
      })}
    >
      <div className="form-check">
        <Checkbox
          checked={selected}
          disabled={disabled}
          id={itemId}
          onChange={(event) => {
            changeSelection(thread.id, event.target.checked)
          }}
        />
        <div>
          <label className="selected-threads-thread-title" htmlFor={itemId}>
            {thread.title}
          </label>
          {error ? (
            <ThreadValidationError error={error}>
              {({ message }) => <FieldError>{message}</FieldError>}
            </ThreadValidationError>
          ) : (
            <Tidbits small>
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
          )}
        </div>
      </div>
    </li>
  )
}

export default ThreadsModerationSelectedThreadsListItem
