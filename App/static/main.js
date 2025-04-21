
async function getUserData(){
    const response = await fetch('/api/users');
    return response.json();
}

function loadTable(users){
    const table = document.querySelector('#result');
    for(let user of users){
        table.innerHTML += `<tr>
            <td>${user.id}</td>
            <td>${user.username}</td>
        </tr>`;
    }
}

async function main(){
    const users = await getUserData();
    loadTable(users);
}

// Connect to the Socket.IO server
const socket = io('/notifications');

socket.on('connect', () => {
    console.log('Connected to SocketIO');

    const userId = window.USER_ID;

    if (userId) {
        socket.emit('join', { user_id: userId });
    } else {
        console.error('User ID not available');
    }
});

// Listen for expiration alerts
socket.on('expiration_alert', (data) => {
    Swal.fire({
        title: 'Expiration Alert',
        text: data.message,
        icon: 'warning',
        confirmButtonText: 'OK'
    });
});

main();
