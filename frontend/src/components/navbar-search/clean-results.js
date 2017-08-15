const MAX_RESULTS = 5;

export default function(data) {
  const filtered = data.filter((section) => {
    return section.results.count > 0;
  });

  return filtered.map((section) => {
    return Object.assign({}, section, {
      results: section.results.results.slice(0, MAX_RESULTS)
    });
  });
}