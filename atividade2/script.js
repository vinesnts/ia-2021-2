document.getElementById('submeter').addEventListener('click', (e) => {
  e.preventDefault();
  const search_type = document.getElementById('search_type').value;
  const graph = document.getElementById('graph').value;
  const origin = document.getElementById('origin').value;
  const destiny = document.getElementById('destiny').value;
  fetch('http://127.0.0.1:8000/graph', {
    headers: {
      'Content-Type': 'application/json',
    },
    method: 'POST',
    body: JSON.stringify({
      'search_type': search_type,
      'graph': graph,
      'origin': origin,
      'destiny': destiny,
    }),
  }).then((res) => {
    res.json().then((json) => {
      let img = document.querySelector('.img-response');
      if (img) {
        img.remove();
      }
      img = document.createElement('img');
      img.classList.add('img-response')
      img.src = `data:image/png;base64,${json['payload']}`;
      document.querySelector('.resposta').appendChild(img);
      console.log(json);
    }).catch((error) => {
      throw error;
    });
  }).catch((error) => {
    console.log(error);
  });
});