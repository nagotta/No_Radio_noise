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

// コーナーの削除処理
document.getElementById('deletionForm').addEventListener('submit', function(e) {
    e.preventDefault();

    if (confirm('本当に削除してもよろしいですか？')) {
        var radioName = document.getElementById('radioSelect').value;
        var cornerName = document.getElementById('cornerSelect').value;
        sendDeleteRequest('/delete_corner', { radioName: radioName, cornerName: cornerName });
    }
});

// ラジオ選択時にコーナーメニューを更新
document.getElementById('radioSelect').addEventListener('change', function() {
    var radioName = this.value;

    fetch('/get_corners/' + encodeURIComponent(radioName))
        .then(function(response) {
            if (!response.ok) {
                throw new Error('HTTP error ' + response.status);
            }
            return response.json();
        })
        .then(function(corners) {
            var cornerSelect = document.getElementById('cornerSelect');
            // 既存の選択肢をクリア
            while (cornerSelect.firstChild) {
                cornerSelect.firstChild.remove();
            }
            // 新しい選択肢を追加
            corners.forEach(function(corner) {
                var option = document.createElement('option');
                option.value = corner;
                option.textContent = corner;
                cornerSelect.appendChild(option);
            });
        })
        .catch(function(error) {
            console.error('エラー:', error);
        });
});
