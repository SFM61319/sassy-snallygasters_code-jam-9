const webSocket = new WebSocket('ws://localhost:8000');
const contactServerButton = document.getElementById('contact-server-button');

webSocket.addEventListener('open', (e) => {
  webSocket.send('Connection established.');
});

webSocket.addEventListener('message', (e) => {
  console.log(e.data);
});

contactServerButton?.addEventListener('click', (e) => {
  webSocket.send('Initialize.');
});
