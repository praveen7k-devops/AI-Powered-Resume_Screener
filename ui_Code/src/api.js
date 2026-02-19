export async function predictCandidate(name) {
  //const url = `http://127.0.0.1:8000/predict?name=${encodeURIComponent(name)}`;

  const url = 'http://127.0.0.1:8000/predict';

  console.log('Sending name to API:', name);

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ name }),
  });

  if (!response.ok) {
    throw new Error('API request failed');
  }

  return await response.json();
}
