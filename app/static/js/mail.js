document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var radioName = document.getElementById('radioSelect').value;
    var cornerName = document.getElementById('cornerSelect').value;
    var content = document.getElementById('content').value;

    fetch('/mail', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'radioName': radioName,
            'cornerName': cornerName,
            'content': content
        })
    })
    .then(function(response) {
        if (!response.ok) {
            throw new Error('HTTP error ' + response.status);
        }
        return response.json();
    })
    .then(function(data) {
        if (data.success) {
            window.close(); 
        } else {
            console.error('メール送信に失敗しました:', data.error);
        }
    })
    .catch(function(error) {
        console.error('エラー:', error);
    });
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
