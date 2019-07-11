// socketIO | for channel.html
            document.addEventListener('DOMContentLoaded', () => {
                //connect to websocket
                var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

              

                // configure 
                //when connected, configure buttons
                socket.on('connect', () => {
                    // button should emit 'send message' event
                    document.querySelector("#submit-message").onclick = () => {
                        const message = document.querySelector("#message").value;
                        socket.emit('send message', {"message": message});
                    };
                });
            });

            //when a message is sent, add it to html
            socket.on('announce message', data => {
                const li = document.createElement('li');
                li.innerHTML = `${data.message}`;
                document.querySelector("#messages").append(li);
            });
