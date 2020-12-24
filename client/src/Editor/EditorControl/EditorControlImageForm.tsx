import { Trans } from "@lingui/macro"
import React from "react"
import * as Yup from "yup"
import { Field, FieldError, Form, FormFooter } from "../../UI/Form"
import Input from "../../UI/Input"
import { ModalFormBody, ModalFooter } from "../../UI/Modal"
import { LinkValidationError } from "../../UI/ValidationError"
import { IEditorContextValues } from "../EditorContext"

interface IEditorControlImageFormProps {
  context: IEditorContextValues
  close: () => void
}

interface FormValues {
  link: string
  label: string
}

const EditorControlImageForm: React.FC<IEditorControlImageFormProps> = ({
  context,
  close,
}) => {
  const validators = Yup.object().shape({
    link: Yup.string().required("value_error.missing").url("value_error.link"),
    label: Yup.string(),
  })

  return (
    <Form<FormValues>
      id="editor_image_form"
      defaultValues={{ link: "", label: "" }}
      validators={validators}
      onSubmit={({ data: { link, label } }) => {
        context.replaceSelection({
          replace: label.trim()
            ? `![${label.trim()}](${link.trim()})`
            : `!(${link.trim()})`,
        })

        close()
      }}
    >
      <ModalFormBody>
        <Field
          label={<Trans id="editor.image_modal.link">Link to image</Trans>}
          name="link"
          input={<Input />}
          error={(error, value) => (
            <LinkValidationError error={error} value={value}>
              {({ message }) => <FieldError>{message}</FieldError>}
            </LinkValidationError>
          )}
        />
        <Field
          label={
            <Trans id="editor.image_modal.label">Image label (optional)</Trans>
          }
          name="label"
          input={<Input />}
        />
      </ModalFormBody>
      <ModalFooter>
        <FormFooter submitText={<Trans id="ok">Ok</Trans>} onCancel={close} />
      </ModalFooter>
    </Form>
  )
}

export default EditorControlImageForm
