document.addEventListener("htmx:afterSettle", () => {
  const root = document.getElementById("misago-snackbars")
  root.querySelectorAll(".snackbar").forEach((element) => {
    element.classList.add("in")
  })
})
