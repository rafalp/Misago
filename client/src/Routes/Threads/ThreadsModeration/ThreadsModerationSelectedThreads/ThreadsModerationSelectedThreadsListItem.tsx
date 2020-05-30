import React from "react"
import {
  Checkbox,
  TidbitCategory,
  TidbitReplies,
  Tidbits,
} from "../../../../UI"
import { ISelectedThread } from "./ThreadsModerationSelectedThreads.types"

interface IThreadsModerationSelectedThreadsListItemProps {
  disabled?: boolean
  id?: string
  selected?: boolean
  thread: ISelectedThread
  changeSelection: (id: string, selected: boolean) => void
}

const ThreadsModerationSelectedThreadsListItem: React.FC<IThreadsModerationSelectedThreadsListItemProps> = ({
  disabled,
  id,
  selected,
  thread,
  changeSelection,
}) => {
  const itemId = id ? id + "_" + thread.id : undefined

  return (
    <li className="selected-threads-thread">
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
        </div>
      </div>
    </li>
  )
}

export default ThreadsModerationSelectedThreadsListItem
