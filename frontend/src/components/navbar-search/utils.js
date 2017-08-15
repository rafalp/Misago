export function getSuggestions(data) {
  return data.filter((section) => {
    return section.results.count > 0;
  });
}

export function getSectionSuggestions(section) {
  return section.results.results.map((item) => {
    return Object.assign({}, item, { section });
  });
}

export function renderSectionTitle(section) {
  return section.name;
}
