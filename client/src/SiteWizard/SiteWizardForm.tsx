import { Trans, t } from "@lingui/macro"
import React from "react"
import * as Yup from "yup"
import { useSettingsContext } from "../Context"
import { CardAlert, CardFormBody, CardFooter } from "../UI/Card"
import { Field, FieldError, Form, FormFooter } from "../UI/Form"
import Input from "../UI/Input"
import RootError from "../UI/RootError"
import Select from "../UI/Select"
import {
  EmailValidationError,
  PasswordValidationError,
  UsernameValidationError,
  ValidationError,
} from "../UI/ValidationError"
import SiteWizardContainer from "./SiteWizardContainer"
import { useAuth } from "../auth"
import useSetupSiteMutation from "./useSetupSiteMutation"

interface FormValues {
  forumName: string
  forumIndexThreads: string
  name: string
  email: string
  password: string
}

interface SiteWizardFormProps {
  complete: () => void
}

const SiteWizardForm: React.FC<SiteWizardFormProps> = ({ complete }) => {
  const { login } = useAuth()
  const settings = useSettingsContext()
  const [setupSite, { loading, error: graphqlError }] = useSetupSiteMutation()

  if (!settings) return null

  const validators = Yup.object().shape({
    forumName: Yup.string()
      .required("value_error.missing")
      .min(1, "value_error.any_str.min_length")
      .max(150, "value_error.any_str.max_length"),
    name: Yup.string()
      .required("value_error.missing")
      .min(settings.usernameMinLength, "value_error.any_str.min_length")
      .max(settings.usernameMaxLength, "value_error.any_str.max_length")
      .matches(/^[a-zA-Z0-9]+$/, "value_error.username"),
    password: Yup.string()
      .required("value_error.missing")
      .min(settings.passwordMinLength, "value_error.any_str.min_length")
      .max(settings.passwordMaxLength, "value_error.any_str.max_length"),
    email: Yup.string()
      .required("value_error.missing")
      .email("value_error.email"),
  })

  return (
    <SiteWizardContainer>
      <Form<FormValues>
        id="setup_site_form"
        disabled={loading}
        defaultValues={{
          forumName: "Misago",
          forumIndexThreads: "threads",
          name: "",
          email: "",
          password: "",
        }}
        validators={validators}
        onSubmit={async ({ clearErrors, setError, data: input }) => {
          clearErrors()

          try {
            const result = await setupSite({
              variables: {
                input: Object.assign({}, input, {
                  forumIndexThreads: input.forumIndexThreads === "threads",
                }),
              },
            })
            const { errors, user, token } = result.data?.setupSite || {}

            if (errors) {
              errors?.forEach(({ location, type, message }) => {
                const field = location.join(".") as
                  | "forumName"
                  | "forumIndexThreads"
                  | "name"
                  | "email"
                  | "password"
                setError(field, { type, message })
              })
            } else {
              if (user && token) {
                login({ token, user, preserveStore: true })
              }
              complete()
            }
          } catch (error) {
            // do nothing when setupSite throws
            return
          }
        }}
      >
        <RootError graphqlError={graphqlError}>
          {({ message }) => <CardAlert>{message}</CardAlert>}
        </RootError>
        <CardFormBody>
          <fieldset>
            <legend>
              <Trans id="wizard.site">Site</Trans>
            </legend>
            <Field
              label={<Trans id="wizard.forum_name">Forum name</Trans>}
              name="forumName"
              input={<Input maxLength={150} />}
              error={(error, value) => (
                <ValidationError
                  error={error}
                  value={value.trim().length}
                  min={1}
                  max={150}
                >
                  {({ message }) => <FieldError>{message}</FieldError>}
                </ValidationError>
              )}
            />
            <Field
              label={<Trans id="wizard.forum_index">Forum index</Trans>}
              name="forumIndexThreads"
              input={
                <Select
                  options={[
                    {
                      value: "threads",
                      name: t({
                        id: "wizard.forum_index.threads",
                        message: "Latest threads",
                      }),
                    },
                    {
                      value: "categories",
                      name: t({
                        id: "wizard.forum_index.categories",
                        message: "Categories",
                      }),
                    },
                  ]}
                />
              }
              error={(error, value) => (
                <ValidationError error={error} value={value.trim().length}>
                  {({ message }) => <FieldError>{message}</FieldError>}
                </ValidationError>
              )}
            />
          </fieldset>
          <fieldset>
            <legend>
              <Trans id="wizard.admin">Admin account</Trans>
            </legend>
            <Field
              label={<Trans id="input.name">User name</Trans>}
              name="name"
              input={<Input maxLength={settings.usernameMaxLength} />}
              error={(error, value) => (
                <UsernameValidationError
                  error={error}
                  value={value.trim().length}
                  min={settings.usernameMinLength}
                  max={settings.usernameMaxLength}
                >
                  {({ message }) => <FieldError>{message}</FieldError>}
                </UsernameValidationError>
              )}
            />
            <Field
              label={<Trans id="input.email">E-mail</Trans>}
              name="email"
              input={<Input maxLength={100} type="email" />}
              error={(error) => (
                <EmailValidationError error={error}>
                  {({ message }) => <FieldError>{message}</FieldError>}
                </EmailValidationError>
              )}
            />
            <Field
              label={<Trans id="input.password">Password</Trans>}
              name="password"
              input={
                <Input
                  maxLength={settings.passwordMaxLength}
                  type="password"
                />
              }
              error={(error, value) => (
                <PasswordValidationError
                  error={error}
                  value={value.length}
                  min={settings.passwordMinLength}
                  max={settings.passwordMaxLength}
                >
                  {({ message }) => <FieldError>{message}</FieldError>}
                </PasswordValidationError>
              )}
            />
          </fieldset>
        </CardFormBody>
        <CardFooter>
          <FormFooter
            loading={loading}
            submitText={<Trans id="wizard.continue">Continue</Trans>}
          />
        </CardFooter>
      </Form>
    </SiteWizardContainer>
  )
}

export default SiteWizardForm
