import { MockedProvider } from "@apollo/react-testing"
import { I18nProvider } from "@lingui/react"
import { actions } from "@storybook/addon-actions"
import React from "react"
import Navbar from "."
import { RootContainer } from "../UI/Storybook"
import { IAvatar } from "../types"

export default {
  title: "Navbar",
}

const navbarActions = actions({
  openLogin: "open login",
  openRegister: "open register",
})
const avatarSizes: Array<number> = [400, 200, 150, 100, 64, 50, 30]

const getAvatars = (): Array<IAvatar> => {
  let avatars: Array<IAvatar> = []
  avatarSizes.forEach(size => {
    avatars.push({
      size,
      url: `https://placekitten.com/g/${size}/${size}`,
    })
  })
  return avatars
}

const settings = {
  forumName: "Misago",
}

const user = {
  id: "1",
  name: "JohnDoe",
  avatars: getAvatars(),
}

export const Anonymous = () => (
  <MockedProvider>
    <I18nProvider language="en">
      <RootContainer>
        <Navbar settings={settings} user={null} {...navbarActions} />
      </RootContainer>
    </I18nProvider>
  </MockedProvider>
)

export const Authenticated = () => (
  <MockedProvider>
    <I18nProvider language="en">
      <RootContainer>
        <Navbar settings={settings} user={user} {...navbarActions} />
      </RootContainer>
    </I18nProvider>
  </MockedProvider>
)
