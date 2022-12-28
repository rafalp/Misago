export default function (bytes) {
  if (bytes > 1024 * 1024 * 1024) {
    return roundSize(bytes / (1024 * 1024 * 1024)) + " GB"
  } else if (bytes > 1024 * 1024) {
    return roundSize(bytes / (1024 * 1024)) + " MB"
  } else if (bytes > 1024) {
    return roundSize(bytes / 1024) + " KB"
  } else {
    return roundSize(bytes) + " B"
  }
}

export function roundSize(value) {
  return value.toFixed(1)
}
