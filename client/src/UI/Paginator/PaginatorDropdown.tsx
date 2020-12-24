import { Trans } from "@lingui/macro"
import classnames from "classnames"
import React from "react"
import { ButtonSecondary } from "../Button"
import { Dropdown } from "../Dropdown"
import { PaginatorProps } from "./Paginator.types"
import PaginatorDropdownMenu from "./PaginatorDropdownMenu"

interface PaginatorDropdownProps extends PaginatorProps {
  compact?: boolean
}

const PaginatorDropdown: React.FC<PaginatorDropdownProps> = ({
  compact,
  page,
  pages,
  url,
}) => (
  <Dropdown
    className="paginator-dropdown"
    placement="bottom"
    toggle={({ ref, toggle }) => (
      <ButtonSecondary
        className={classnames("btn-secondary", "btn-paginator-toggle", {
          "btn-paginator-toggle-compact": compact,
          "btn-paginator-toggle-full": !compact,
        })}
        elementRef={ref}
        text={
          compact ? (
            <Trans id="paginator_compact">
              {page} of {pages}
            </Trans>
          ) : (
            <Trans id="paginator">
              Page {page} of {pages}
            </Trans>
          )
        }
        icon={!compact ? "fas fa-ellipsis-v" : undefined}
        responsive
        onClick={toggle}
      />
    )}
    menu={({ close }) => (
      <PaginatorDropdownMenu
        close={close}
        page={page}
        pages={pages}
        url={url}
      />
    )}
    resistant
  />
)

export default PaginatorDropdown
