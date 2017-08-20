import { HEADER, RESULT, FOOTER } from './contants';

export default function(results) {
  const flatlist = [];
  flattenProviders(results, flatlist);
  return flatlist;
}

function flattenProviders(results, flatlist) {
  const arrayLength = results.length;
  for (var i = 0; i < arrayLength; i++) {
    const provider = results[i];

    flatlist.push({
      provider,
      type: HEADER
    });

    flattenProvider(provider, flatlist);
  }
}

function flattenProvider(provider, flatlist) {
  const arrayLength = provider.results.length;
  for (var i = 0; i < arrayLength; i++) {
    const result = provider.results[i];
    flatlist.push({
      provider,
      result,
      type: RESULT
    });
  }

  flatlist.push({
    provider,
    type: FOOTER
  });
}