function sendDeleteRequest(endpoint, data) {
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(function(response) {
        if (!response.ok) {
            throw new Error('HTTP error ' + response.status);
        }
        return response.json();
    })
    .then(function(json) {
        alert('削除が成功しました');
        window.close();
    })
    .catch(function(error) {
        alert('削除が失敗しました: ' + error.message);
    });
}

// ラジオの削除処理
document.getElementById('deletionFormRadio').addEventListener('submit', function(e) {
    e.preventDefault();

    if (confirm('本当に削除してもよろしいですか？')) {
        var radioName = document.getElementById('radioSelect').value;
        sendDeleteRequest('/delete_radio', { radioName: radioName });
    }
});
