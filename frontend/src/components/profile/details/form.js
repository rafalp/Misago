import React from "react"
import Form from "misago/components/edit-details"

export default function ({ api, display, onCancel, onSuccess }) {
  if (!display) return null

  return <Form api={api} onCancel={onCancel} onSuccess={onSuccess} />
}
