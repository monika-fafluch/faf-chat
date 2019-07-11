// channels page | get a user's name from localStorage
document.addEventListener('DOMContentLoaded', () => {
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

    // save a channel's name in localStorage
    document.querySelector("#create-channel-form").onsubmit = () => {
        const channel = document.querySelector("#create-channel").value;
        localStorage.setItem('channel', channel);
        //store channels names
            
    };


});