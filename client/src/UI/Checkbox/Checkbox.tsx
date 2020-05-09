import React from "react"

interface ICheckboxProps {
  checked?: boolean
  disabled?: boolean
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void
}

const Checkbox: React.FC<ICheckboxProps> = ({
  checked,
  disabled,
  onChange,
}) => (
  <input
    className="form-check-input"
    type="checkbox"
    checked={checked}
    disabled={disabled}
    onChange={onChange}
  />
)

export default Checkbox
