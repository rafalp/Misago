import React from "react"
import { connect } from "react-redux"
import { close } from "../../reducers/overlay"
import { Overlay, OverlayHeader } from "../Overlay"
import SiteNavMenu from "./SiteNavMenu"

export function SiteNavOverlay({ dispatch, isOpen }) {
  return (
    <Overlay open={isOpen}>
      <OverlayHeader>{pgettext("site nav title", "Menu")}</OverlayHeader>
      <SiteNavMenu close={() => dispatch(close())} overlay />
    </Overlay>
  )
}

function select(state) {
  return {
    isOpen: state.overlay.siteNav,
  }
}

const SiteNavOverlayConnected = connect(select)(SiteNavOverlay)

export default SiteNavOverlayConnected
