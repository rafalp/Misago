import React from "react"
import { Layout, LayoutSide } from "../Layout"
import { RootContainer } from "../Storybook"
import SideNav from "./SideNav"
import SideNavItem from "./SideNavItem"

export default {
  title: "UI/SideNav",
}

export const Default = () => (
  <RootContainer padding>
    <Layout>
      <LayoutSide>
        <SideNav>
          <SideNavItem to="/">
            Lorem ipsum
          </SideNavItem>
          <SideNavItem to="/" hasChildren>
            Dolor met
          </SideNavItem>
          <SideNavItem to="/">
            Sit amet
          </SideNavItem>
        </SideNav>
      </LayoutSide>
    </Layout>
  </RootContainer>
)

export const ActiveItem = () => (
  <RootContainer padding>
    <Layout>
      <LayoutSide>
        <SideNav>
          <SideNavItem to="/">
            Lorem ipsum
          </SideNavItem>
          <SideNavItem to="/" isActive>
            Dolor met
          </SideNavItem>
          <SideNavItem to="/">
            Sit amet
          </SideNavItem>
        </SideNav>
      </LayoutSide>
    </Layout>
  </RootContainer>
)

export const ActiveItemWithChild = () => (
  <RootContainer padding>
    <Layout>
      <LayoutSide>
        <SideNav>
          <SideNavItem to="/">
            Lorem ipsum
          </SideNavItem>
          <SideNavItem to="/" isActive hasChildren>
            Dolor met
          </SideNavItem>
          <SideNavItem to="/" isChild>
            Nihi novi
          </SideNavItem>
          <SideNavItem to="/">
            Sit amet
          </SideNavItem>
        </SideNav>
      </LayoutSide>
    </Layout>
  </RootContainer>
)

export const ItemWithActiveChild = () => (
  <RootContainer padding>
    <Layout>
      <LayoutSide>
        <SideNav>
          <SideNavItem to="/">
            Lorem ipsum
          </SideNavItem>
          <SideNavItem to="/" isActive hasChildren>
            Dolor met
          </SideNavItem>
          <SideNavItem to="/" isActive isChild>
            Nihi novi
          </SideNavItem>
          <SideNavItem to="/">
            Sit amet
          </SideNavItem>
        </SideNav>
      </LayoutSide>
    </Layout>
  </RootContainer>
)