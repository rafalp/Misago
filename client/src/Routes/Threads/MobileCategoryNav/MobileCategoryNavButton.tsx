import { Trans } from "@lingui/macro"
import React from "react"
import {
  ButtonJustified,
  CategoryIcon,
  Icon,
  Toolbar,
  ToolbarItem,
} from "../../../UI"
import { IActiveCategory } from "../Threads.types"
import { ThreadsCategoryModalContext } from "../ThreadsCategoryModalContext"

interface IMobileCategoryNavButtonProps {
  active?: IActiveCategory | null
}

const MobileCategoryNavButton: React.FC<IMobileCategoryNavButtonProps> = ({
  active,
}) => {
  const { open } = React.useContext(ThreadsCategoryModalContext)

  return (
    <Toolbar mobile tablet>
      <ToolbarItem fill>
        <ButtonJustified
          left={
            <CategoryIcon
              className="btn-category-icon"
              category={active?.category}
            />
          }
          center={
            active ? (
              active.category.name
            ) : (
              <Trans id="threads.header">All threads</Trans>
            )
          }
          right={
            <span className="btn-more-icon">
              <Icon icon="ellipsis-v" fixedWidth solid />
            </span>
          }
          onClick={() => open(active)}
          responsive
        />
      </ToolbarItem>
    </Toolbar>
  )
}

export default MobileCategoryNavButton
