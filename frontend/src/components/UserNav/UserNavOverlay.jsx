import React from "react"
import { connect } from "react-redux"
import { close } from "../../reducers/overlay"
import { DropdownFooter } from "../Dropdown"
import { Overlay, OverlayHeader } from "../Overlay"
import UserNavMenu from "./UserNavMenu"
import logout from "./logout"

export function UserNavOverlay({ dispatch, isOpen }) {
  return (
    <Overlay open={isOpen}>
      <OverlayHeader>
        {pgettext("user nav title", "Your options")}
      </OverlayHeader>
      <UserNavMenu close={() => dispatch(close())} overlay />
      <DropdownFooter>
        <button
          className="btn btn-default btn-block"
          onClick={() => {
            logout()
            dispatch(close())
          }}
          type="button"
        >
          {pgettext("user nav", "Log out")}
        </button>
      </DropdownFooter>
    </Overlay>
  )
}

function select(state) {
  return {
    isOpen: state.overlay.userNav,
  }
}

const UserNavOverlayConnected = connect(select)(UserNavOverlay)

export default UserNavOverlayConnected
