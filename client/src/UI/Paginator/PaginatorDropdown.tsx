import { Trans } from "@lingui/macro"
import React from "react"
import { Dropdown } from "../Dropdown"
import { IPaginatorProps } from "./Paginator.types"
import PaginatorDropdownMenu from "./PaginatorDropdownMenu"

const PaginatorDropdown: React.FC<IPaginatorProps> = ({
  page,
  pages,
  url,
}) => (
  <Dropdown
    className="paginator-dropdown"
    placement="bottom"
    toggle={({ ref, toggle }) => (
      <button
        type="button"
        className="btn btn-secondary btn-responsive"
        ref={ref}
        onClick={toggle}
      >
        <Trans id="paginator">
          Page {page} of {pages}
        </Trans>
      </button>
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
