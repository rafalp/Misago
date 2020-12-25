import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonJustified } from "../../../UI/Button"
import CategoryIcon from "../../../UI/CategoryIcon"
import Icon from "../../../UI/Icon"
import { Toolbar, ToolbarItem } from "../../../UI/Toolbar"
import { IActiveCategory } from "../Threads.types"
import { useThreadsCategoriesModalContext } from "./ThreadsCategoriesModalContext"

interface ThreadsCategoriesModalButtonProps {
  active?: IActiveCategory | null
}

const ThreadsCategoriesModalButton: React.FC<ThreadsCategoriesModalButtonProps> = ({
  active,
}) => {
  const { open } = useThreadsCategoriesModalContext()

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
              <Icon icon="fas fa-ellipsis-v" fixedWidth />
            </span>
          }
          onClick={() => open(active)}
          responsive
        />
      </ToolbarItem>
    </Toolbar>
  )
}

export default ThreadsCategoriesModalButton
