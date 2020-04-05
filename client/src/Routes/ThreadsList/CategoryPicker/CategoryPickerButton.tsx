import { Trans } from "@lingui/macro"
import React from "react"
import { CategoryIcon, Icon } from "../../../UI"

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
  <button
    className="btn btn-secondary btn-justified"
    type="button"
    onClick={onClick}
  >
    <span className="btn-justified-left">
      <CategoryIcon category={active} />
    </span>
    <span className="btn-justified-center">
      {active ? active.name : <Trans id="threads.header">All threads</Trans>}
    </span>
    <span className="btn-justified-right">
      <span className="btn-more-icon">
        <Icon icon="ellipsis-v" fixedWidth solid />
      </span>
    </span>
  </button>
)

export default CategoryPickerButton
