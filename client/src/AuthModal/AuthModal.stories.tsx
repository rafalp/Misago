import { MockedProvider } from "@apollo/react-testing"
import { actions } from "@storybook/addon-actions"
import React from "react"
import { Modal } from "../UI/Modal"
import { RootContainer } from "../UI/Storybook"
import LoginModal from "./LoginModal"
import RegisterModal from "./RegisterModal"

export default {
  title: "Auth/Modal",
}

const { close, showLogin, showRegister } = actions({
  close: "close modal",
  showLogin: "show login form",
  showRegister: "show register form",
})

const settings = {
  passwordMinLength: 5,
  passwordMaxLength: 20,
  usernameMinLength: 2,
  usernameMaxLength: 10,
}

export const Login = () => (
  <MockedProvider>
    <RootContainer>
      <Modal isOpen={true} close={close}>
        <LoginModal close={close} showRegister={showRegister} />
      </Modal>
    </RootContainer>
  </MockedProvider>
)

export const Register = () => (
  <MockedProvider>
    <RootContainer>
      <Modal isOpen={true} close={close}>
        <RegisterModal
          settings={settings}
          close={close}
          showLogin={showLogin}
        />
      </Modal>
    </RootContainer>
  </MockedProvider>
)
