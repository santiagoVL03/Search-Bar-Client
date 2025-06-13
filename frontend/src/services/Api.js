export async function fetchSearchResults(query) {
  const url = `http://localhost:5000/api/v1/search/?word=${encodeURIComponent(query)}`
  const response = await fetch(url)

  if (!response.ok) {
    throw new Error('Network response was not ok')
  }

  return response.json()
}
