import { Trans } from "@lingui/macro"
import classnames from "classnames"
import React from "react"
import { useFormContext } from "react-hook-form"
import { useFieldContext } from "../UI/Form"
import EditorBody from "./EditorBody"
import EditorButton from "./EditorButton"
import EditorPreview from "./EditorPreview"
import EditorPreviewButton from "./EditorPreviewButton"
import EditorToolbar from "./EditorToolbar"

interface IEditorProps {
  name?: string
  disabled?: boolean
  submit?: React.ReactNode
}

const Editor: React.FC<IEditorProps> = ({ name, disabled, submit }) => {
  const context = useFieldContext()
  const hookContext = useFormContext()
  const [preview, setPreview] = React.useState<string | null>(null)

  const finName = name || context.name

  if (!hookContext) return null
  if (!finName) return null

  const openPreview = () => {
    const value = hookContext.getValues(finName) || ""
    if (value.trim().length > 0) {
      setPreview(value.trim())
    }
  }

  const closePreview = () => setPreview(null)

  return (
    <EditorBody disabled={disabled || context.disabled}>
      {preview && <EditorPreview markup={preview} />}
      <textarea
        className={classnames(
          "form-control form-control-responsive form-editor-textarea",
          {
            "d-none": preview,
            "is-invalid": context.invalid,
          }
        )}
        disabled={disabled || context.disabled}
        name={name || context.name}
        ref={hookContext.register}
      />
      <EditorToolbar>
        <div className="row">
          <div className="col" />
          <div className="col-auto">
            {preview ? (
              <EditorButton
                disabled={disabled || context.disabled}
                onClick={closePreview}
              >
                <Trans id="editor.write">Write</Trans>
              </EditorButton>
            ) : (
              <EditorPreviewButton
                disabled={disabled || context.disabled}
                name={finName}
                onClick={openPreview}
              />
            )}
            {submit}
          </div>
        </div>
      </EditorToolbar>
    </EditorBody>
  )
}

export default Editor
