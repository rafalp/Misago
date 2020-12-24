import { Trans } from "@lingui/macro"
import React from "react"
import { useHistory } from "react-router-dom"
import { DropdownContainer, DropdownHeader } from "../Dropdown"
import { PaginatorProps } from "./Paginator.types"

interface PaginatorDropdownMenuProps extends PaginatorProps {
  close: () => void
}

const PaginatorDropdownMenu: React.FC<PaginatorDropdownMenuProps> = ({
  close,
  page,
  pages,
  url,
}) => {
  const [state, setState] = React.useState("")
  const history = useHistory()

  return (
    <form
      onSubmit={(event) => {
        if (page) {
          let number = Number.parseInt(state)
          if (isNaN(number)) number = page
          if (number < 1) number = 1
          if (number > pages) number = pages

          if (number !== page) {
            history.push(url(number))
          }
        }

        close()
        event.preventDefault()
        return false
      }}
    >
      <DropdownHeader text={<Trans id="paginator.goto">Go to page</Trans>} />
      <DropdownContainer>
        <div className="paginator-goto">
          <input
            className="form-control form-control-sm"
            type="number"
            max={pages}
            min="1"
            step="1"
            value={state}
            onChange={({ target }) => setState(target.value)}
          />
          <button className="btn btn-sm btn-primary">
            <Trans id="go">Go</Trans>
          </button>
        </div>
      </DropdownContainer>
    </form>
  )
}

export default PaginatorDropdownMenu
