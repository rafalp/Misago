import { Trans } from "@lingui/macro"
import classnames from "classnames"
import React from "react"
import { useFormContext } from "react-hook-form"
import { useFieldContext } from "../UI/Form"
import EditorBody from "./EditorBody"
import EditorButton from "./EditorButton"
import EditorPreview from "./EditorPreview"
import EditorToolbar from "./EditorToolbar"

interface IEditorProps {
  name?: string
  disabled?: boolean
}

const Editor: React.FC<IEditorProps> = ({ name, disabled }) => {
  const context = useFieldContext()
  const hookContext = useFormContext() || {}
  const [preview, setPreview] = React.useState<string | null>(null)

  if (!hookContext) return null
  if (!name && !context.name) return null

  const openPreview = () => {
    const value = hookContext.getValues(name || context.name || "") || ""
    if (value.trim().length > 0) {
      setPreview(value.trim())
    }
  }

  const closePreview = () => setPreview(null)

  return (
    <EditorBody disabled={disabled || context.disabled}>
      <EditorToolbar>
        {preview ? (
          <EditorButton
            disabled={disabled || context.disabled}
            onClick={closePreview}
          >
            <Trans id="editor.write">Write</Trans>
          </EditorButton>
        ) : (
          <EditorButton
            disabled={disabled || context.disabled}
            onClick={openPreview}
          >
            <Trans id="editor.preview">Preview</Trans>
          </EditorButton>
        )}
      </EditorToolbar>
      {preview && <EditorPreview markup={preview} />}
      <div className={classnames({ "d-none": preview })}>
        <textarea
          className={classnames("form-control form-editor-textarea", {
            "is-invalid": context.invalid,
          })}
          disabled={disabled || context.disabled}
          name={name || context.name}
          ref={hookContext.register}
          rows={5}
        />
      </div>
    </EditorBody>
  )
}

export default Editor
