
window.onload = ((e) => {
  document.getElementById('textoFormGroup').style = 'display:none;'
  document.getElementById('fileTextoFormGroup').style = 'display:none;'
  // document.getElementById('wikipediaTextoFormGroup').style = 'display:none;'
});

document.getElementById('source').addEventListener('change', (e) => {
  const value = e.target.value;
  const textos = document.querySelectorAll('*[name="texto"]');
  let texto = '';
  textos.forEach((e) => {
    if (e.value) {
      e.value  = '';
    }
  });
  document.getElementById('textoFormGroup').style = 'display:none;'
  document.getElementById('fileTextoFormGroup').style = 'display:none;'
  document.getElementById('wikipediaTextoFormGroup').style = 'display:none;'

  if (value === 'w') {
    document.getElementById('wikipediaTextoFormGroup').style = 'display:block;'
  } else if (value === 'a') {
    document.getElementById('fileTextoFormGroup').style = 'display:block;'
  } else if (value === 'i') {
    document.getElementById('textoFormGroup').style = 'display:block;'
  }
});

document.getElementById('submeter').addEventListener('click', (e) => {
  e.preventDefault();
  const source = document.getElementById('source').value;
  const textos = document.querySelectorAll('*[name="texto"]');
  let texto = '';
  textos.forEach((e) => {
    if (e.value) {
      texto = e.value;
    }
  });
  fetch('http://127.0.0.1:8000/separar', {
    headers: {
      'Content-Type': 'application/json',
    },
    method: 'POST',
    body: JSON.stringify({
      'source': source,
      'text': texto,
    }),
  }).then((res) => {
    res.json().then((json) => {
      console.log(json);
      document.getElementById('verb').innerText = `Qtd. de verbos: ${json.payload?.VERB[0]}, verbos: ${json.payload?.VERB[1]}`;
      document.getElementById('conj').innerText = `Qtd. de conjunções: ${json.payload?.CCONJ[0]}, conjunções: ${json.payload?.CCONJ[1]}`;
      document.getElementById('subProp').innerText = `Qtd. de substantivos próprios: ${json.payload?.PROPN[0]}, substantivos próprios: ${json.payload?.PROPN[1]}`;
      document.getElementById('subCom').innerText = `Qtd. de substantivos comuns: ${json.payload?.NOUN[0]}, substantivos comuns: ${json.payload?.NOUN[1]}`;
      document.getElementById('pron').innerText = `Qtd. de pronomes: ${json.payload?.PRON[0]}, pronomes: ${json.payload?.PRON[1]}`;
    }).catch((error) => {
      throw error;
    });
  }).catch((error) => {
    console.log(error);
  });
});