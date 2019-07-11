// execute when DOM content is loaded                                                           // index page
 document.addEventListener('DOMContentLoaded', () => {
    //save user's name in localStorage
    document.querySelector("#form").onsubmit = () => {
        const name = document.querySelector("#name").value;
        localStorage.setItem('name', name);
    };
                                                                                                // create-channel page

    // retrieve user's name from localStorage and say hello
    const name = localStorage.getItem('name');
    document.querySelector("#hello-name").innerHTML = 'Hello' + ' ' + name;
    
    // disable submit button be defult and if no input
    document.querySelector("#submit").disabled = true;
    document.querySelector("#create-channel").onkeyup = () => {
        if (document.querySelector("#create-channel").value.length > 0)
            document.querySelector("#submit").disabled = false;
        else
            document.querySelector("#submit").disabled = true;
    };

    // save channel's name in localStorage to take the user back to that channel later
    document.querySelector("#create-channel-form").onsubmit = () => {
        const channel = document.querySelector("#create-channel").value;
        localStorage.setItem('last channel', channel);
    };
                                                                                                // channels page
    // join the channel chosen from the channels list
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.on('connect', () => {
        // clicking the link should emit 'join' event
        document.querySelectorAll('button').forEach(button => {
            button.onclick = () => {
                alert("ok");
                const room = button.innerHTML;
                const username = localStorage.getItem('name');
                alert(room); //CHECK IF ROOM AND USERNAME IS PASSED TO 'JOIN' IN SERVER !!!!!!!!!!!!!!!!!
                socket.emit('join', {"room": room, "username": username});
            };
        });
    });

    // configure button to send messages after joining some channel
    socket.on('join', () => {
        document.querySelector("#submit-message").onclick = () => {
            
            const message = document.querySelector("#message").value;
            const room = document.querySelector("#specific-channel").innerHTML;
            var date = new Date();
            date = date.getDate() + '/' + (date.getMonth() + 1) + '/' + date.getFullYear() +  
                    ' ' + '|' + ' ' + date.getHours() + ":" + date.getMinutes();
            socket.emit('send message', {"message": message, "room": room, "date": date})
        };
    });

    // create <li> to display messages after emitting 'announce message' by the server
    socket.on('announce message', data => {
        const li = document.createElement('li');
        li.innerHTML = `(${data.date} ${data.name}: ${data.message})`;
        alert(li.innerHTML);
        document.querySelector("#messages").append(li);
        document.querySelector("#message").value = "";
    })
});
