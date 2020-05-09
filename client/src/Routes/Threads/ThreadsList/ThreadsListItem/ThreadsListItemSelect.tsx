import React from "react"
import { Checkbox } from "../../../../UI"

interface IThreadsListItemSelectProps {
  selected: boolean
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void
}

const ThreadsListItemSelect: React.FC<IThreadsListItemSelectProps> = ({
  selected,
  onChange,
}) => (
  <div className="col-auto threads-list-select">
    <Checkbox checked={selected} onChange={onChange} />
  </div>
)

export default ThreadsListItemSelect
