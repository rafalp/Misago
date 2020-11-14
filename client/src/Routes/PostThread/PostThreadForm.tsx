import { Trans, t } from "@lingui/macro"
import { useLingui } from "@lingui/react"
import React from "react"
import { Redirect } from "react-router-dom"
import * as Yup from "yup"
import {
  useAuthContext,
  useSettingsContext,
  useToastsContext,
} from "../../Context"
import {
  Card,
  CardAlert,
  CardFooter,
  CardFormBody,
  CardHeader,
} from "../../UI/Card"
import { Checkbox } from "../../UI/Checkbox"
import { Field, FieldError, Form, FormFooter } from "../../UI/Form"
import Input from "../../UI/Input"
import RootError from "../../UI/RootError"
import {
  CategoryValidationError,
  ThreadTitleValidationError,
  ValidationError,
} from "../../UI/ValidationError"
import * as urls from "../../urls"
import { ICategoryChoice } from "./PostThread.types"
import PostThreadCategoryInput from "./PostThreadCategoryInput"
import usePostThreadMutation from "./usePostThreadMutation"

const Editor = React.lazy(() => import("../../Editor"))

interface IPostThreadFormProps {
  category?: string
  categories: Array<ICategoryChoice>
  validCategories: Array<string>
}

interface IPostThreadFormValues {
  category: string
  title: string
  markup: string
  isClosed: boolean
}

const PostThreadForm: React.FC<IPostThreadFormProps> = ({
  category,
  categories,
  validCategories,
}) => {
  const { i18n } = useLingui()

  const user = useAuthContext()
  const isModerator = user ? user.isModerator : false

  const { showToast } = useToastsContext()
  const {
    postMinLength,
    threadTitleMaxLength,
    threadTitleMinLength,
  } = useSettingsContext()
  const [
    postThread,
    { data, loading, error: graphqlError },
  ] = usePostThreadMutation()

  const PostThreadSchema = Yup.object().shape({
    category: Yup.string().required("value_error.missing"),
    title: Yup.string()
      .required("value_error.thread_title.missing")
      .min(threadTitleMinLength, "value_error.any_str.min_length")
      .max(threadTitleMaxLength, "value_error.any_str.max_length")
      .matches(/[a-zA-Z0-9]/, "value_error.thread_title"),
    markup: Yup.string()
      .required("value_error.missing")
      .min(postMinLength, "value_error.any_str.min_length"),
  })

  if (data?.postThread.thread) {
    return <Redirect to={urls.thread(data.postThread.thread)} />
  }

  return (
    <Card>
      <CardHeader title={<Trans id="posting.form">Post a new thread</Trans>} />
      <Form<IPostThreadFormValues>
        defaultValues={{
          category: category || "",
          title: "",
          markup: "",
          isClosed: false,
        }}
        disabled={loading}
        validators={PostThreadSchema}
        onSubmit={async ({ clearErrors, setError, data: input }) => {
          clearErrors()

          const result = await postThread({ variables: { input } })
          const { errors, thread } = result.data?.postThread || {}

          errors?.forEach(({ location, type, message }) => {
            const field = location.join(".") as
              | "markup"
              | "title"
              | "category"
              | "isClosed"
            setError(field, { type, message })
          })

          if (thread) {
            showToast(
              <Trans id="posting.message">New thread has been posted.</Trans>
            )
          }
        }}
      >
        <RootError
          graphqlError={graphqlError}
          dataErrors={data?.postThread.errors}
        >
          {({ message }) => <CardAlert>{message}</CardAlert>}
        </RootError>
        <CardFormBody>
          <Field
            label={<Trans id="posting.thread_title">Thread title</Trans>}
            name="title"
            input={
              <Input
                placeholder={i18n._("posting.thread_title", t`Thread title`)}
                responsive
              />
            }
            error={(error, value) => (
              <ThreadTitleValidationError
                error={error}
                value={value.trim().length}
                min={threadTitleMinLength}
                max={threadTitleMaxLength}
              >
                {({ message }) => <FieldError>{message}</FieldError>}
              </ThreadTitleValidationError>
            )}
            labelReaderOnly
          />
          <Field
            label={<Trans id="posting.thread_category">Thread category</Trans>}
            name="category"
            input={
              <PostThreadCategoryInput
                choices={categories}
                validChoices={validCategories}
                responsive
              />
            }
            error={(error) => (
              <CategoryValidationError error={error}>
                {({ message }) => <FieldError>{message}</FieldError>}
              </CategoryValidationError>
            )}
            labelReaderOnly
          />
          <Field
            label={<Trans id="posting.message">Message contents</Trans>}
            name="markup"
            input={<Editor />}
            error={(error, value) => (
              <ValidationError
                error={error}
                value={value.trim().length}
                min={postMinLength}
              >
                {({ message }) => <FieldError>{message}</FieldError>}
              </ValidationError>
            )}
            labelReaderOnly
          />
          {isModerator && (
            <Field
              label={
                <Trans id="posting.close_thread">Post thread as closed</Trans>
              }
              name="isClosed"
              input={<Checkbox />}
              error={(error) => (
                <ValidationError error={error}>
                  {({ message }) => <FieldError>{message}</FieldError>}
                </ValidationError>
              )}
              check
            />
          )}
        </CardFormBody>
        <CardFooter>
          <FormFooter
            submitText={<Trans id="posting.submit">Post thread</Trans>}
          />
        </CardFooter>
      </Form>
    </Card>
  )
}

export default PostThreadForm
