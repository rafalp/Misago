import { Trans } from "@lingui/macro"
import React from "react"
import {
  ButtonJustified,
  CategoryIcon,
  Icon,
  Toolbar,
  ToolbarItem,
} from "../../../UI"

interface IMobileCategoryNavButtonProps {
  active?: {
    id: string
    name: string
    color: string | null
    icon: string | null
  } | null
  onClick: () => void
}

const MobileCategoryNavButton: React.FC<IMobileCategoryNavButtonProps> = ({
  active,
  onClick,
}) => (
  <Toolbar mobile tablet>
    <ToolbarItem fill>
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
        responsive
      />
    </ToolbarItem>
  </Toolbar>
)

export default MobileCategoryNavButton
