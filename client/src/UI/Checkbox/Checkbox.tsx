import React from "react"

interface ICheckboxProps {
  checked?: boolean
  disabled?: boolean
  id?: string
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void
}

const Checkbox: React.FC<ICheckboxProps> = ({
  checked,
  disabled,
  id,
  onChange,
}) => (
  <span className="form-check-input">
    <input
      id={id}
      type="checkbox"
      checked={checked}
      disabled={disabled}
      onChange={onChange}
    />
  </span>
)

export default Checkbox
