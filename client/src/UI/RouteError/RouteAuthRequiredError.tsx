import { Trans } from "@lingui/macro"
import classnames from "classnames"
import React from "react"
import { useAuthModalContext } from "../../Context"
import { ButtonPrimary } from "../Button"
import { Error } from "../Error"
import RouteContainer from "../RouteContainer"
import WindowTitle from "../WindowTitle"

interface RouteErrorProps {
  className?: string | null
  header?: React.ReactNode
  message?: React.ReactNode
}

const RouteAuthRequiredError: React.FC<RouteErrorProps> = ({
  className,
  header,
  message,
}) => {
  const { openLoginModal, openRegisterModal } = useAuthModalContext()

  return (
    <RouteContainer
      className={classnames("route-auth-error-container", className)}
    >
      <WindowTitle />
      <Error
        className="route-auth"
        header={
          header || (
            <Trans id="auth_error.title">
              You must be logged in to access this page.
            </Trans>
          )
        }
        message={
          message || (
            <Trans id="auth_error.message">
              Please log in or sign up to continue.
            </Trans>
          )
        }
        action={
          <>
            <ButtonPrimary
              text={<Trans id="login">Log in</Trans>}
              responsive
              onClick={openLoginModal}
            />
            <ButtonPrimary
              text={<Trans id="register">Sign up</Trans>}
              responsive
              onClick={openRegisterModal}
            />
          </>
        }
      />
    </RouteContainer>
  )
}

export default RouteAuthRequiredError
