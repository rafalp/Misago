import classNames from "classnames"
import React from "react"

interface IThreadsListItemSelectProps {
  selected: boolean
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void
}

const ThreadsListItemSelect: React.FC<IThreadsListItemSelectProps> = ({
  selected,
  onChange,
}) => (
  <div className={classNames("col-auto threads-list-select")}>
    <input
      className="form-check-input"
      type="checkbox"
      checked={selected}
      onChange={onChange}
    />
  </div>
)

export default ThreadsListItemSelect
