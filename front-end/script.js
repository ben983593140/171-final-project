const pts = document.querySelector('#PTS');
const twop = document.querySelector('#TP');
const twopa = document.querySelector('#TPA');
const fga = document.querySelector('#FGA');
const ws = document.querySelector('#WS');
const fg = document.querySelector('#FG');
const submitBtn = document.getElementById("submit-btn");
let pts_D, twop_D, twopa_D, fga_D, gs_D, fg_D;
pts.addEventListener('input', function() {
  pts_D = parseFloat(pts.value);
})

twop.addEventListener('input', function() {
  twop_D = parseFloat(twop.value);
})

twopa.addEventListener('input', function() {
  twopa_D = parseFloat(twopa.value);
})

fga.addEventListener('input', function() {
  fga_D = parseFloat(fga.value);
})

fg.addEventListener('input', function() {
  fg_D = parseFloat(fg.value);
})

ws.addEventListener('input', function() {
  ws_D = parseFloat(ws.value);
})
submitBtn.addEventListener('click', function() {
  fetchData();
});


async function fetchData() {
  let b = await fetch("http://127.0.0.1:5000/", {
    method: "POST",
    body: JSON.stringify({
      ws: ws_D,
      twopa: twopa_D,
      fga: fga_D,
      twop: twop_D,
      pts: pts_D,
      fg: fg_D
    }),
    headers: {
      "Content-type": "application/json",
      Accept: "application/json",
    },
  });
  console.log(await b.json());

};