export default async function getHttpResponseErrorMessage(response) {
  if (
    typeof response.getResponseHeader !== "undefined" &&
    response.getResponseHeader("content-type") === "application/json"
  ) {
    const data = JSON.parse(response.response)
    if (data.error) {
      return data.error
    }
  } else if (response.headers.get("content-type") === "application/json") {
    const data = await response.json()
    if (data.error) {
      return data.error
    }
  }

  if (response.status === 404) {
    return pgettext("htmx response error", "Page not found")
  }

  if (response.status === 403) {
    return pgettext("htmx response error", "Permission denied")
  }

  if (response.status === 0) {
    return pgettext("htmx response error", "Site could not be reached")
  }

  return pgettext("htmx response error", "Unexpected error")
}
