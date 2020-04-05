import { Trans } from "@lingui/macro"
import React from "react"

interface ICategoryPickerButtonProps {
  active?: {
    id: string
    name: string
    color: string | null
    icon: string | null
  }
  onClick: () => void
}

const CategoryPickerButton: React.FC<ICategoryPickerButtonProps> = ({
  active,
  onClick,
}) => (
  <button type="button" onClick={onClick}>
    {active ? active.name : <Trans id="threads.header">All threads</Trans>}
  </button>
)

export default CategoryPickerButton
