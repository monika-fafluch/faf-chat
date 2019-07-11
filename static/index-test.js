document.addEventListener("DOMContentLoaded", () => {
    console.log("dom");
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.on('connect', () => {
        socket.send('User has connected');
    });
    // 'user has connectes' message
    socket.on('message_me', msg => {
        const li = document.createElement('li');
        li.innerHTML = msg;
        document.querySelector("#messages").append(li);
    });
    // click event on button to send messages
    document.querySelector("#sendbutton").onclick = () => {
        alert("click works");
        console.log("onclick works");
        const message = document.querySelector("#myMessage").value;
        socket.send(message);
        document.querySelector("#myMessage").value = '';
    };
});

