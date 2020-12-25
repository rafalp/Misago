import React from "react"
import { Checkbox } from "../../../../UI/Checkbox"
import { FormCheckbox } from "../../../../UI/Form"

interface ThreadsListItemSelectProps {
  selected: boolean
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void
}

const ThreadsListItemSelect: React.FC<ThreadsListItemSelectProps> = ({
  selected,
  onChange,
}) => (
  <div className="col-auto threads-list-select">
    <FormCheckbox>
      <Checkbox checked={selected} onChange={onChange} />
    </FormCheckbox>
  </div>
)

export default ThreadsListItemSelect
