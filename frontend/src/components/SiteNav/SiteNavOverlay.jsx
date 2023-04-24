import React from "react"
import { connect } from "react-redux"
import { Overlay, OverlayHeader } from "../Overlay"
import SiteNav from "./SiteNav"

export function SiteNavOverlay({ dispatch, isOpen }) {
  return (
    <Overlay open={isOpen}>
      <OverlayHeader>{pgettext("site nav title", "Menu")}</OverlayHeader>
      <SiteNav overlay />
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
