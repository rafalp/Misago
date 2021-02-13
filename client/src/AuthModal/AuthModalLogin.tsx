import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonLink, ButtonPrimary } from "../UI/Button"
import { Field, Form } from "../UI/Form"
import Input from "../UI/Input"
import {
  ModalAlert,
  ModalDialog,
  ModalFooter,
  ModalFormBody,
  ModalHeader,
  ModalSize,
} from "../UI/Modal"
import RootError from "../UI/RootError"
import { useAuth } from "../auth"
import useLoginMutation from "./useLoginMutation"

interface LoginValues {
  username: string
  password: string
}

interface AuthModalLoginProps {
  close: () => void
  showRegister: () => void
}

const AuthModalLogin: React.FC<AuthModalLoginProps> = ({
  close,
  showRegister,
}) => {
  const { login } = useAuth()
  const [disabled, setDisabled] = React.useState<boolean>(false)
  const [error, setError] = React.useState<string | null>(null)
  const [
    authenticate,
    { data, loading, error: graphqlError },
  ] = useLoginMutation()

  return (
    <ModalDialog
      className="modal-dialog-auth modal-dialog-login"
      size={ModalSize.SMALL}
    >
      <ModalHeader
        title={<Trans id="login.title">Log in</Trans>}
        close={close}
      />
      <Form<LoginValues>
        id="login_form"
        defaultValues={{ username: "", password: "" }}
        disabled={loading || disabled}
        onSubmit={async ({ data: variables }) => {
          const { username, password } = variables
          if (!username.trim().length || !password.length) {
            setError("value_error.all_fields_are_required")
            return
          }

          setError(null)

          const result = await authenticate({ variables })
          const { user, token } = result.data?.login || {}
          if (token && user) {
            setDisabled(true)
            login({ token, user })
            close()
          }
        }}
      >
        <RootError
          graphqlError={graphqlError}
          dataErrors={data?.login.errors}
          plainError={error}
          messages={{
            "value_error.all_fields_are_required": (
              <Trans id="value_error.all_fields_are_required">
                Fill out all fields.
              </Trans>
            ),
            "value_error.invalid_credentials": (
              <Trans id="value_errosr.invalid_credentials">
                Login or password is incorrect.
              </Trans>
            ),
          }}
        >
          {({ message }) => <ModalAlert>{message}</ModalAlert>}
        </RootError>
        <ModalFormBody>
          <Field
            label={
              <Trans id="login.input.username">User name or e-mail</Trans>
            }
            name="username"
            input={<Input maxLength={255} />}
          />
          <Field
            label={<Trans id="login.input.password">Password</Trans>}
            name="password"
            input={<Input maxLength={255} type="password" />}
          />
        </ModalFormBody>
        <ModalFooter>
          <ButtonPrimary
            loading={loading || disabled}
            text={
              loading || disabled ? (
                <Trans id="login.submitting">Logging in...</Trans>
              ) : (
                <Trans id="login.submit">Log in</Trans>
              )
            }
            block
          />
          <ButtonLink
            disabled={loading || disabled}
            text={
              <Trans id="login.register">
                Not a member? <strong>Sign up</strong>
              </Trans>
            }
            block
            onClick={showRegister}
          />
        </ModalFooter>
      </Form>
    </ModalDialog>
  )
}

export default AuthModalLogin
