import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonJustified, CategoryIcon, Icon } from "../../../UI"

interface IMobileCategoryNavButtonProps {
  active?: {
    id: string
    name: string
    color: string | null
    icon: string | null
  }
  onClick: () => void
}

const MobileCategoryNavButton: React.FC<IMobileCategoryNavButtonProps> = ({
  active,
  onClick,
}) => (
  <ButtonJustified
    left={<CategoryIcon className="btn-category-icon" category={active} />}
    center={
      active ? active.name : <Trans id="threads.header">All threads</Trans>
    }
    right={
      <span className="btn-more-icon">
        <Icon icon="ellipsis-v" fixedWidth solid />
      </span>
    }
    onClick={onClick}
  />
)

export default MobileCategoryNavButton
