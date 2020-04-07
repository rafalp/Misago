import { useMutation } from "@apollo/react-hooks"
import { Trans } from "@lingui/macro"
import { gql } from "apollo-boost"
import React from "react"
import {
  Button,
  ButtonLink,
  Field,
  Form,
  Input,
  ModalAlert,
  ModalDialog,
  ModalFooter,
  ModalFormBody,
  ModalHeader,
  ModalSize,
  RootError,
} from "../UI"
import { useAuth } from "../auth"
import { IMutationError } from "../types"

const LOGIN = gql`
  mutation Login($username: String!, $password: String!) {
    login(username: $username, password: $password) {
      errors {
        location
        message
        type
      }
      user {
        id
        name
      }
      token
    }
  }
`

interface ILoginData {
  login: {
    errors: Array<IMutationError> | null
    user: {
      id: string
      name: string
    } | null
    token: string | null
  }
}

interface ILoginValues {
  username: string
  password: string
}

interface ILoginModalProps {
  close: () => void
  showRegister: () => void
}

const LoginModal: React.FC<ILoginModalProps> = ({ close, showRegister }) => {
  const { login } = useAuth()
  const [disabled, setDisabled] = React.useState<boolean>(false)
  const [error, setError] = React.useState<string | null>(null)
  const [authenticate, { data, loading, error: graphqlError }] = useMutation<
    ILoginData,
    ILoginValues
  >(LOGIN, { errorPolicy: "all" })

  return (
    <ModalDialog
      className="modal-dialog-auth modal-dialog-login"
      size={ModalSize.SMALL}
    >
      <ModalHeader
        title={<Trans id="login.title">Log in</Trans>}
        close={close}
      />
      <Form<ILoginValues>
        id="login_form"
        defaultValues={{ username: "", password: "" }}
        disabled={loading || disabled}
        onSubmit={async ({ data: variables }) => {
          const { username, password } = variables
          if (!username.trim().length || !password.length) {
            setError("value_error.all_fields_are_required")
            return
          }

          const data = await authenticate({ variables })
          const { user, token } = data.data?.login || {}
          if (token && user) {
            setDisabled(true)
            login(token, user)
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
              <Trans>Fill out all fields.</Trans>
            ),
            "value_error.invalid_credentials": (
              <Trans>Login or password is incorrect.</Trans>
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
          <Button
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

export default LoginModal
